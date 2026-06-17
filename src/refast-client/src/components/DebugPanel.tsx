import React, { useState, useEffect, useRef, useMemo } from 'react';
import { refastBus } from '../utils/eventBus';
import { useEventManager } from '../events/EventManager';

interface DebugMessage {
  direction: 'in' | 'out';
  message: any;
  timestamp: number;
  id: string;
}

interface DebugError {
  type: string;
  message: string;
  timestamp: number;
  details?: any;
  id: string;
}

// Helper component to display formatted JSON payloads with toggle collapse
function JsonValue({ value, depth = 0 }: { value: any; depth?: number }) {
  const [isExpanded, setIsExpanded] = useState(depth < 2);

  if (value === null) return <span className="text-gray-400">null</span>;
  if (value === undefined) return <span className="text-gray-400">undefined</span>;

  if (typeof value === 'boolean') {
    return <span className={value ? 'text-green-500 font-semibold' : 'text-rose-500 font-semibold'}>{value ? 'true' : 'false'}</span>;
  }

  if (typeof value === 'number') {
    return <span className="text-amber-500 font-mono">{value}</span>;
  }

  if (typeof value === 'string') {
    return <span className="text-emerald-500 font-mono">"{value}"</span>;
  }

  if (Array.isArray(value)) {
    if (value.length === 0) return <span className="text-gray-400">[]</span>;
    return (
      <span className="font-mono">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-indigo-400 hover:text-indigo-300 font-bold focus:outline-none"
        >
          {isExpanded ? '▼' : '▶'} Array[{value.length}]
        </button>
        {isExpanded && (
          <div className="pl-4 border-l border-zinc-700/50 my-1">
            {value.map((val, idx) => (
              <div key={idx} className="flex py-0.5">
                <span className="text-zinc-500 mr-2">{idx}:</span>
                <JsonValue value={val} depth={depth + 1} />
              </div>
            ))}
          </div>
        )}
      </span>
    );
  }

  if (typeof value === 'object') {
    const keys = Object.keys(value);
    if (keys.length === 0) return <span className="text-gray-400">{"{}"}</span>;
    return (
      <span className="font-mono">
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-indigo-400 hover:text-indigo-300 font-bold focus:outline-none"
        >
          {isExpanded ? '▼' : '▶'} Object
        </button>
        {isExpanded && (
          <div className="pl-4 border-l border-zinc-700/50 my-1">
            {keys.map((key) => (
              <div key={key} className="flex py-0.5">
                <span className="text-purple-400 mr-2 font-medium">{key}:</span>
                <JsonValue value={value[key]} depth={depth + 1} />
              </div>
            ))}
          </div>
        )}
      </span>
    );
  }

  return <span>{String(value)}</span>;
}

export default function DebugPanel() {
  const { websocket } = useEventManager();
  const [messages, setMessages] = useState<DebugMessage[]>([]);
  const [errors, setErrors] = useState<DebugError[]>([]);
  const [isOpen, setIsOpen] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const [isMaximized, setIsMaximized] = useState(false);
  const [activeTab, setActiveTab] = useState<'ws' | 'errors'>('ws');
  const [wsSearch, setWsSearch] = useState('');
  const [errorSearch, setErrorSearch] = useState('');
  const [expandedMessageId, setExpandedMessageId] = useState<string | null>(null);
  const [expandedErrorId, setExpandedErrorId] = useState<string | null>(null);
  const [newErrorCount, setNewErrorCount] = useState(0);
  const [pulseError, setPulseError] = useState(false);

  // Dragging state for floating action button
  const [btnPosition, setBtnPosition] = useState({ x: 24, y: 24 });
  const isDragging = useRef(false);
  const dragStart = useRef({ x: 0, y: 0 });
  const btnStart = useRef({ x: 0, y: 0 });

  // Listen to messages and errors
  useEffect(() => {
    const unsubMessage = refastBus.on('refast:debug-message', (detail) => {
      setMessages((prev) => {
        const newMessage: DebugMessage = {
          direction: detail.direction,
          message: detail.message,
          timestamp: detail.timestamp,
          id: Math.random().toString(36).substring(2, 9),
        };
        // Cap at 150 items
        const list = [newMessage, ...prev];
        return list.slice(0, 150);
      });
    });

    const unsubError = refastBus.on('refast:debug-error', (detail) => {
      setErrors((prev) => {
        const newErr: DebugError = {
          type: detail.type,
          message: detail.message,
          timestamp: detail.timestamp,
          details: detail.details,
          id: Math.random().toString(36).substring(2, 9),
        };
        // Cap at 50 items
        const list = [newErr, ...prev];
        return list.slice(0, 50);
      });

      // UI Indicator
      setNewErrorCount((c) => c + 1);
      setPulseError(true);
      setTimeout(() => setPulseError(false), 1500);
    });

    return () => {
      unsubMessage();
      unsubError();
    };
  }, []);

  // Clear counters when opening errors tab
  useEffect(() => {
    if (isOpen && activeTab === 'errors') {
      setNewErrorCount(0);
    }
  }, [isOpen, activeTab]);

  // Drag handlers for the floating button
  const handleMouseDown = (e: React.MouseEvent) => {
    // Only drag with left click
    if (e.button !== 0) return;
    isDragging.current = false;
    dragStart.current = { x: e.clientX, y: e.clientY };
    btnStart.current = { ...btnPosition };

    document.addEventListener('mousemove', handleMouseMove);
    document.addEventListener('mouseup', handleMouseUp);
  };

  const handleMouseMove = (e: MouseEvent) => {
    const deltaX = dragStart.current.x - e.clientX;
    const deltaY = dragStart.current.y - e.clientY;
    
    // Set dragging threshold (5px)
    if (Math.hypot(deltaX, deltaY) > 5) {
      isDragging.current = true;
    }

    if (isDragging.current) {
      const newX = Math.max(12, Math.min(window.innerWidth - 70, btnStart.current.x + deltaX));
      const newY = Math.max(12, Math.min(window.innerHeight - 70, btnStart.current.y + deltaY));
      setBtnPosition({ x: newX, y: newY });
    }
  };

  const handleMouseUp = () => {
    document.removeEventListener('mousemove', handleMouseMove);
    document.removeEventListener('mouseup', handleMouseUp);
  };

  const handleButtonClick = () => {
    if (!isDragging.current) {
      setIsOpen(!isOpen);
    }
  };

  const handleResend = (msg: any) => {
    if (websocket && websocket.readyState === WebSocket.OPEN) {
      websocket.send(JSON.stringify(msg));
    } else {
      alert('WebSocket is not connected. Cannot resend message.');
    }
  };

  // Filters
  const filteredMessages = useMemo(() => {
    if (!wsSearch) return messages;
    const searchLower = wsSearch.toLowerCase();
    return messages.filter((m) => {
      const typeStr = String(m.message?.type || '').toLowerCase();
      const contentStr = JSON.stringify(m.message).toLowerCase();
      return typeStr.includes(searchLower) || contentStr.includes(searchLower);
    });
  }, [messages, wsSearch]);

  const filteredErrors = useMemo(() => {
    if (!errorSearch) return errors;
    const searchLower = errorSearch.toLowerCase();
    return errors.filter((e) => {
      const typeStr = e.type.toLowerCase();
      const messageStr = e.message.toLowerCase();
      const detailStr = JSON.stringify(e.details || '').toLowerCase();
      return typeStr.includes(searchLower) || messageStr.includes(searchLower) || detailStr.includes(searchLower);
    });
  }, [errors, errorSearch]);

  return (
    <>
      {/* Floating Action Button */}
      <button
        onMouseDown={handleMouseDown}
        onClick={handleButtonClick}
        style={{
          bottom: `${btnPosition.y}px`,
          right: `${btnPosition.x}px`,
          zIndex: 9999,
        }}
        className={`fixed flex items-center justify-center w-12 h-12 rounded-full cursor-pointer select-none shadow-lg outline-none focus:outline-none transition-all duration-300 border backdrop-blur-md ${
          pulseError 
            ? 'bg-rose-600/90 border-rose-500 text-white animate-pulse ring-4 ring-rose-500/30' 
            : isOpen 
              ? 'bg-zinc-800/90 border-zinc-700 text-indigo-400 hover:text-indigo-300' 
              : 'bg-zinc-900/80 border-zinc-800 text-zinc-300 hover:text-white hover:scale-105 hover:bg-zinc-900/95'
        }`}
        title="Open Refast DevTools"
      >
        {pulseError ? (
          // Warning/Alert icon when error pulses
          <svg className="w-5 h-5 animate-bounce" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
        ) : (
          // Bug/insect icon
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <rect width="8" height="14" x="8" y="5" rx="4" fill="currentColor" fillOpacity={isOpen ? 0.3 : 0.1} />
            <path strokeLinecap="round" strokeLinejoin="round" d="M19 7a1 1 0 00-1-1h-2M4 7a1 1 0 011-1h2M18 11h2M4 11h2M19 15a1 1 0 01-1 1h-2M4 15a1 1 0 001 1h2M12 5V3M10 3h4" />
          </svg>
        )}

        {/* Error Badge */}
        {newErrorCount > 0 && (
          <span className="absolute -top-1.5 -right-1.5 flex h-5 w-5 items-center justify-center rounded-full bg-rose-500 text-[10px] font-bold text-white ring-2 ring-zinc-900">
            {newErrorCount}
          </span>
        )}
      </button>

      {/* Main DevTools Window */}
      {isOpen && !isMinimized && (
        <div
          style={{ zIndex: 9998 }}
          className={`fixed bottom-20 right-6 flex flex-col backdrop-blur-xl bg-zinc-950/95 border border-zinc-800 text-zinc-100 shadow-2xl rounded-2xl overflow-hidden transition-all duration-200 select-none ${
            isMaximized ? 'w-[75vw] h-[75vh]' : 'w-[480px] h-[580px]'
          }`}
        >
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 bg-zinc-900/50 border-b border-zinc-800 cursor-default">
            <div className="flex items-center space-x-2">
              <span className="w-2.5 h-2.5 rounded-full bg-indigo-500 animate-pulse" />
              <h3 className="font-semibold text-sm tracking-wide text-zinc-300">Refast Developer Console</h3>
            </div>
            
            {/* Window Controls */}
            <div className="flex items-center space-x-2">
              {/* Maximize */}
              <button
                onClick={() => setIsMaximized(!isMaximized)}
                className="p-1 rounded text-zinc-400 hover:bg-zinc-800 hover:text-white transition-colors"
                title={isMaximized ? 'Restore window size' : 'Maximize window'}
              >
                {isMaximized ? (
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 9h6v6M9 15h6v-6" />
                  </svg>
                ) : (
                  <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M4 8V4h4M16 4h4v4M4 16v4h4M16 20h4v-4" />
                  </svg>
                )}
              </button>
              
              {/* Minimize */}
              <button
                onClick={() => setIsMinimized(true)}
                className="p-1 rounded text-zinc-400 hover:bg-zinc-800 hover:text-white transition-colors"
                title="Minimize DevTools"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M18 12H6" />
                </svg>
              </button>

              {/* Close */}
              <button
                onClick={() => setIsOpen(false)}
                className="p-1 rounded text-zinc-400 hover:bg-rose-500/30 hover:text-rose-400 transition-colors"
                title="Close DevTools"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>

          {/* Navigation & Search Bar */}
          <div className="flex flex-col px-4 py-2 border-b border-zinc-900 bg-zinc-900/20">
            <div className="flex items-center justify-between">
              <div className="flex space-x-1.5">
                <button
                  onClick={() => setActiveTab('ws')}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition-all ${
                    activeTab === 'ws'
                      ? 'bg-indigo-600 text-white shadow'
                      : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/40'
                  }`}
                >
                  WS Frames ({messages.length})
                </button>
                <button
                  onClick={() => setActiveTab('errors')}
                  className={`relative px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition-all ${
                    activeTab === 'errors'
                      ? 'bg-rose-600 text-white shadow'
                      : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/40'
                  }`}
                >
                  Errors ({errors.length})
                  {errors.length > 0 && activeTab !== 'errors' && (
                    <span className="absolute -top-1 -right-1 flex h-2 w-2 rounded-full bg-rose-500 animate-ping" />
                  )}
                </button>
              </div>

              {/* Clear logs button */}
              <button
                onClick={() => {
                  if (activeTab === 'ws') setMessages([]);
                  else setErrors([]);
                }}
                className="text-[10px] text-zinc-500 hover:text-zinc-300 font-semibold px-2 py-1 rounded border border-zinc-800 hover:border-zinc-700 hover:bg-zinc-900"
              >
                Clear Logs
              </button>
            </div>

            {/* Search inputs */}
            <div className="mt-2 relative">
              <input
                type="text"
                placeholder={activeTab === 'ws' ? 'Filter by type or body...' : 'Filter errors...'}
                value={activeTab === 'ws' ? wsSearch : errorSearch}
                onChange={(e) => activeTab === 'ws' ? setWsSearch(e.target.value) : setErrorSearch(e.target.value)}
                className="w-full text-xs bg-zinc-900/60 border border-zinc-800/80 rounded-lg px-8 py-1.5 focus:outline-none focus:border-indigo-500 text-zinc-200 placeholder-zinc-500"
              />
              <svg className="absolute left-2.5 top-2 w-3.5 h-3.5 text-zinc-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
              {(activeTab === 'ws' ? wsSearch : errorSearch) && (
                <button
                  onClick={() => activeTab === 'ws' ? setWsSearch('') : setErrorSearch('')}
                  className="absolute right-2.5 top-2 text-zinc-500 hover:text-zinc-300"
                >
                  ✕
                </button>
              )}
            </div>
          </div>

          {/* Log Window */}
          <div className="flex-1 overflow-y-auto p-4 space-y-2.5">
            {activeTab === 'ws' ? (
              filteredMessages.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-48 text-zinc-500">
                  <svg className="w-10 h-10 mb-2 opacity-40" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <p className="text-xs">No WebSocket messages recorded</p>
                </div>
              ) : (
                filteredMessages.map((m) => {
                  const isExpanded = expandedMessageId === m.id;
                  const type = m.message?.type || 'unknown';
                  const timestampStr = new Date(m.timestamp).toLocaleTimeString();
                  const isOut = m.direction === 'out';

                  return (
                    <div
                      key={m.id}
                      className={`border rounded-xl bg-zinc-900/40 hover:bg-zinc-900/60 overflow-hidden transition-all ${
                        isExpanded ? 'border-indigo-500/50 bg-zinc-900/60' : 'border-zinc-800/60'
                      }`}
                    >
                      {/* Summary Row */}
                      <div
                        onClick={() => setExpandedMessageId(isExpanded ? null : m.id)}
                        className="flex items-center justify-between p-3 cursor-pointer select-none"
                      >
                        <div className="flex items-center space-x-2.5 min-w-0">
                          {/* Direction Indicator */}
                          <span
                            className={`flex items-center justify-center w-5 h-5 rounded-full text-[10px] font-bold ${
                              isOut 
                                ? 'bg-sky-500/10 text-sky-400 border border-sky-500/20' 
                                : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                            }`}
                          >
                            {isOut ? '↑' : '↓'}
                          </span>

                          <span className="font-mono text-[11px] font-bold text-zinc-300 truncate">
                            {type}
                          </span>
                        </div>

                        <div className="flex items-center space-x-2">
                          <span className="text-[10px] text-zinc-500 font-medium font-mono">{timestampStr}</span>
                          <span className="text-zinc-500 text-xs font-bold">{isExpanded ? '▲' : '▼'}</span>
                        </div>
                      </div>

                      {/* Expandable Payload Viewer */}
                      {isExpanded && (
                        <div className="px-4 pb-4 pt-1 border-t border-zinc-900/60 bg-zinc-950/60 text-xs space-y-3">
                          <div className="flex justify-between items-center text-[10px] text-zinc-400 bg-zinc-900/40 p-1.5 rounded border border-zinc-800/40">
                            <span>Direction: <strong className={isOut ? 'text-sky-400' : 'text-emerald-400'}>{isOut ? 'Client OUT (Send)' : 'Server IN (Receive)'}</strong></span>
                            {isOut && type === 'callback' && (
                              <button
                                onClick={(e) => {
                                  e.stopPropagation();
                                  handleResend(m.message);
                                }}
                                className="px-2 py-0.5 bg-indigo-600 hover:bg-indigo-500 text-white rounded font-bold text-[9px]"
                              >
                                Replay Msg
                              </button>
                            )}
                          </div>
                          
                          <div className="max-h-60 overflow-y-auto text-left leading-relaxed">
                            <JsonValue value={m.message} />
                          </div>
                        </div>
                      )}
                    </div>
                  );
                })
              )
            ) : (
              filteredErrors.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-48 text-zinc-500">
                  <svg className="w-10 h-10 mb-2 opacity-40" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={1.5}>
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <p className="text-xs">No errors recorded. Nice job!</p>
                </div>
              ) : (
                filteredErrors.map((e) => {
                  const isExpanded = expandedErrorId === e.id;
                  const timeStr = new Date(e.timestamp).toLocaleTimeString();
                  const isCritical = e.type.includes('Exception') || e.type.includes('Error');

                  return (
                    <div
                      key={e.id}
                      className={`border rounded-xl bg-zinc-900/30 hover:bg-zinc-900/50 overflow-hidden transition-all ${
                        isExpanded ? 'border-rose-500/50 bg-zinc-900/50' : 'border-zinc-800/60'
                      }`}
                    >
                      {/* Summary Row */}
                      <div
                        onClick={() => setExpandedErrorId(isExpanded ? null : e.id)}
                        className="flex items-start justify-between p-3.5 cursor-pointer select-none"
                      >
                        <div className="flex flex-col space-y-1 pr-4 min-w-0">
                          <span
                            className={`inline-block self-start px-2 py-0.5 rounded text-[9px] font-bold uppercase tracking-wider ${
                              isCritical 
                                ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20' 
                                : 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                            }`}
                          >
                            {e.type}
                          </span>
                          <span className="text-xs font-semibold text-zinc-200 line-clamp-2">
                            {e.message}
                          </span>
                        </div>

                        <div className="flex items-center space-x-2 flex-shrink-0">
                          <span className="text-[10px] text-zinc-500 font-medium font-mono">{timeStr}</span>
                          <span className="text-zinc-500 text-xs font-bold">{isExpanded ? '▲' : '▼'}</span>
                        </div>
                      </div>

                      {/* Expandable Detail View */}
                      {isExpanded && (
                        <div className="px-4 pb-4 pt-1 border-t border-zinc-900/60 bg-zinc-950/60 text-xs space-y-3">
                          {e.details?.traceback ? (
                            /* Monospace Traceback Viewer */
                            <div className="space-y-1">
                              <span className="text-[10px] text-zinc-400 font-bold">Python Traceback:</span>
                              <pre className="p-3 bg-zinc-900 rounded-lg text-[10px] text-rose-300 font-mono overflow-x-auto whitespace-pre leading-relaxed select-text max-h-72">
                                {e.details.traceback}
                              </pre>
                            </div>
                          ) : e.details?.stack ? (
                            /* Monospace JS/React Stack Viewer */
                            <div className="space-y-1">
                              <span className="text-[10px] text-zinc-400 font-bold">JS Stack Trace:</span>
                              <pre className="p-3 bg-zinc-900 rounded-lg text-[10px] text-rose-300 font-mono overflow-x-auto whitespace-pre leading-relaxed select-text max-h-72">
                                {e.details.stack}
                              </pre>
                            </div>
                          ) : null}

                          {/* Extra Metadata fields */}
                          {e.details && Object.keys(e.details).some((k) => k !== 'traceback' && k !== 'stack') && (
                            <div className="space-y-1 text-left">
                              <span className="text-[10px] text-zinc-400 font-bold">Metadata:</span>
                              <div className="p-3 bg-zinc-900 rounded-lg max-h-60 overflow-y-auto">
                                <JsonValue 
                                  value={Object.fromEntries(
                                    Object.entries(e.details).filter(([k]) => k !== 'traceback' && k !== 'stack')
                                  )} 
                                />
                              </div>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  );
                })
              )
            )}
          </div>
        </div>
      )}

      {/* Minimized Indicator Bar */}
      {isOpen && isMinimized && (
        <button
          onClick={() => setIsMinimized(false)}
          className="fixed bottom-4 right-6 flex items-center space-x-2 px-3.5 py-2 rounded-xl bg-zinc-900 border border-zinc-800 text-indigo-400 hover:text-indigo-300 shadow-xl cursor-pointer hover:bg-zinc-950 select-none transition-all duration-200"
          style={{ zIndex: 9999 }}
        >
          <span className="w-2 h-2 rounded-full bg-indigo-500 animate-ping" />
          <span className="text-xs font-semibold tracking-wide">Developer Console (Minimized)</span>
          {newErrorCount > 0 && (
            <span className="flex h-4 w-4 items-center justify-center rounded-full bg-rose-500 text-[9px] font-bold text-white">
              {newErrorCount}
            </span>
          )}
        </button>
      )}
    </>
  );
}
