import React, { useCallback, useRef, useState } from 'react';
import { cn } from '../../utils';
import { Icon } from './icon';

// ─── Types ───────────────────────────────────────────────────────────────────

interface PendingFileInfo {
  name: string;
  size: number;
  type: string;
}

interface UploadedFileInfo {
  id: string;
  name: string;
  size: number;
  content_type: string;
}

type FileStatus = 'pending' | 'uploading' | 'complete' | 'error';

interface FileEntry {
  /** Local ID (not the server-side UUID) used only for React keys */
  localId: string;
  file: File;
  status: FileStatus;
  progress: number; // 0–100
  uploadedInfo?: UploadedFileInfo;
  error?: string;
}

interface FileUploaderProps {
  label?: string;
  description?: string;
  variant?: 'dropzone' | 'button';
  disabled?: boolean;
  required?: boolean;
  error?: string;
  accept?: string;
  multiple?: boolean;
  maxSize?: number;
  maxFiles?: number;
  dragDrop?: boolean;
  uploadUrl?: string;
  className?: string;
  name?: string;
  onSelect?: (eventData: { files: PendingFileInfo[] }) => void;
  onUploadStart?: (eventData: { files: PendingFileInfo[] }) => void;
  onUploadComplete?: (eventData: { files: UploadedFileInfo[] }) => void;
  onUploadError?: (eventData: { error: string; file: PendingFileInfo }) => void;
  onRemove?: (eventData: { file: PendingFileInfo }) => void;
  'data-refast-id'?: string;
}

// ─── Helpers ─────────────────────────────────────────────────────────────────

function formatBytes(bytes: number): string {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
}

function toPendingFileInfo(file: File): PendingFileInfo {
  return { name: file.name, size: file.size, type: file.type };
}

let localIdCounter = 0;
function nextLocalId(): string {
  return `fu-${++localIdCounter}`;
}

/** Read a cookie value by name, returning null when absent. */
function getCookie(name: string): string | null {
  const match = document.cookie.match(new RegExp('(?:^|;\\s*)' + name + '=([^;]*)'));
  return match ? decodeURIComponent(match[1]) : null;
}

/**
 * Validate that an upload URL is safe to use.
 * Rejects javascript: and data: schemes; only same-origin or relative paths
 * are accepted.
 */
function isSafeUploadUrl(url: string): boolean {
  try {
    const parsed = new URL(url, window.location.origin);
    // Only allow same-origin URLs (relative or explicitly same origin)
    return parsed.origin === window.location.origin;
  } catch {
    return false;
  }
}

// ─── Sub-components ──────────────────────────────────────────────────────────

interface FileRowProps {
  entry: FileEntry;
  onRemove: () => void;
}

const FileRow: React.FC<FileRowProps> = ({ entry, onRemove }) => {
  const isComplete = entry.status === 'complete';
  const isError = entry.status === 'error';
  const isUploading = entry.status === 'uploading';

  return (
    <div className="flex items-center gap-3 rounded-md border border-border bg-muted/30 px-3 py-2 text-sm">
      {/* File icon */}
      <span className="flex-none text-muted-foreground">
        <Icon name="file" size={16} />
      </span>

      {/* Name + progress */}
      <div className="min-w-0 flex-1">
        <p className="truncate font-medium text-foreground">{entry.file.name}</p>
        <div className="mt-1 flex items-center gap-2">
          <span className="text-xs text-muted-foreground">{formatBytes(entry.file.size)}</span>

          {isUploading && (
            <div className="flex flex-1 items-center gap-2">
              <div className="h-1.5 flex-1 overflow-hidden rounded-full bg-muted">
                <div
                  className="h-full rounded-full bg-primary transition-all duration-150"
                  style={{ width: `${entry.progress}%` }}
                />
              </div>
              <span className="text-xs text-muted-foreground">{entry.progress}%</span>
            </div>
          )}

          {isError && (
            <span className="text-xs text-destructive">{entry.error}</span>
          )}
        </div>
      </div>

      {/* Status icon + remove */}
      <div className="flex flex-none items-center gap-1">
        {isComplete && (
          <span className="text-success">
            <Icon name="check-circle" size={16} />
          </span>
        )}
        {isError && (
          <span className="text-destructive">
            <Icon name="x-circle" size={16} />
          </span>
        )}
        {isUploading && (
          <span className="animate-spin text-primary">
            <Icon name="loader-2" size={16} />
          </span>
        )}
        <button
          type="button"
          onClick={onRemove}
          aria-label={`Remove ${entry.file.name}`}
          className={cn(
            'ml-1 rounded p-0.5 text-muted-foreground transition-colors',
            'hover:bg-muted hover:text-foreground',
            'focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring',
          )}
        >
          <Icon name="x" size={14} />
        </button>
      </div>
    </div>
  );
};

// ─── Main component ───────────────────────────────────────────────────────────

/**
 * FileUploader – upload files via multipart POST with drag-and-drop support.
 *
 * Prop names use camelCase as ComponentRenderer converts snake_case → camelCase.
 */
export const FileUploader: React.FC<FileUploaderProps> = ({
  label = 'Upload file',
  description,
  variant = 'dropzone',
  disabled = false,
  required = false,
  error: serverError,
  accept,
  multiple = false,
  maxSize,
  maxFiles,
  dragDrop = true,
  uploadUrl = '/api/upload',
  className,
  name,
  onSelect,
  onUploadStart,
  onUploadComplete,
  onUploadError,
  onRemove,
  'data-refast-id': dataRefastId,
}) => {
  const [entries, setEntries] = useState<FileEntry[]>([]);
  const [isDragOver, setIsDragOver] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  // ── File validation ──────────────────────────────────────────────────────

  const validateFiles = useCallback(
    (files: File[], currentCount = 0): { valid: File[]; errors: string[] } => {
      const errors: string[] = [];
      let valid = files;

      if (maxFiles !== undefined) {
        const remaining = maxFiles - currentCount;
        if (remaining <= 0) {
          errors.push(`Maximum ${maxFiles} file${maxFiles !== 1 ? 's' : ''} allowed.`);
          return { valid: [], errors };
        }
        if (files.length > remaining) {
          errors.push(`Maximum ${maxFiles} file${maxFiles !== 1 ? 's' : ''} allowed.`);
          valid = files.slice(0, remaining);
        }
      }

      if (maxSize !== undefined) {
        const oversized = valid.filter((f) => f.size > maxSize);
        if (oversized.length > 0) {
          errors.push(
            `${oversized.map((f) => f.name).join(', ')} exceed${oversized.length === 1 ? 's' : ''} the ${formatBytes(maxSize)} size limit.`,
          );
          valid = valid.filter((f) => f.size <= maxSize);
        }
      }

      return { valid, errors };
    },
    [maxFiles, maxSize],
  );

  // ── Upload via XHR ────────────────────────────────────────────────────────

  const uploadEntry = useCallback(
    (entry: FileEntry): Promise<UploadedFileInfo> => {
      return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        const formData = new FormData();
        formData.append('files', entry.file);

        xhr.upload.onprogress = (e) => {
          if (e.lengthComputable) {
            const percent = Math.round((e.loaded / e.total) * 100);
            setEntries((prev) =>
              prev.map((en) => (en.localId === entry.localId ? { ...en, progress: percent } : en)),
            );
          }
        };

        xhr.onload = () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            try {
              const resp: { files: UploadedFileInfo[] } = JSON.parse(xhr.responseText);
              if (!Array.isArray(resp.files) || resp.files.length === 0) {
                throw new Error('Empty files array in server response');
              }
              const uploaded = resp.files[0];
              setEntries((prev) =>
                prev.map((en) =>
                  en.localId === entry.localId
                    ? { ...en, status: 'complete', progress: 100, uploadedInfo: uploaded }
                    : en,
                ),
              );
              resolve(uploaded);
            } catch {
              const msg = 'Invalid server response';
              setEntries((prev) =>
                prev.map((en) =>
                  en.localId === entry.localId ? { ...en, status: 'error', error: msg } : en,
                ),
              );
              reject(new Error(msg));
            }
          } else {
            let msg = `Upload failed (${xhr.status})`;
            try {
              const errBody = JSON.parse(xhr.responseText);
              if (errBody.error) msg = errBody.error;
            } catch {
              // ignore parse errors
            }
            setEntries((prev) =>
              prev.map((en) =>
                en.localId === entry.localId ? { ...en, status: 'error', error: msg } : en,
              ),
            );
            reject(new Error(msg));
          }
        };

        xhr.onerror = () => {
          const msg = 'Network error during upload';
          setEntries((prev) =>
            prev.map((en) =>
              en.localId === entry.localId ? { ...en, status: 'error', error: msg } : en,
            ),
          );
          reject(new Error(msg));
        };

        xhr.open('POST', uploadUrl);

        // Forward the CSRF token when the security middleware has set the cookie.
        const csrfToken = getCookie('csrf_token');
        if (csrfToken) {
          xhr.setRequestHeader('X-CSRF-Token', csrfToken);
        }

        xhr.send(formData);
      });
    },
    [uploadUrl],
  );

  // ── Handle file selection ────────────────────────────────────────────────

  const handleFiles = useCallback(
    async (rawFiles: FileList | File[]) => {
      if (disabled) return;
      setLocalError(null);

      // Reject uploads to URLs that are not same-origin to prevent data exfiltration.
      if (!isSafeUploadUrl(uploadUrl)) {
        setLocalError('Upload URL is not allowed.');
        return;
      }

      const fileArr = Array.from(rawFiles);
      const { valid, errors } = validateFiles(fileArr, entries.length);

      if (errors.length > 0) {
        setLocalError(errors.join(' '));
        if (valid.length === 0) return;
      }

      const newEntries: FileEntry[] = valid.map((file) => ({
        localId: nextLocalId(),
        file,
        status: 'pending',
        progress: 0,
      }));

      const combined = multiple ? [...entries, ...newEntries] : newEntries;
      setEntries(combined);

      onSelect?.({ files: valid.map(toPendingFileInfo) });

      if (valid.length === 0) return;

      // Mark as uploading
      const uploadingEntries = newEntries.map((e) => ({ ...e, status: 'uploading' as FileStatus }));
      setEntries((prev) => {
        const ids = new Set(uploadingEntries.map((e) => e.localId));
        return prev.map((e) => (ids.has(e.localId) ? { ...e, status: 'uploading' } : e));
      });

      onUploadStart?.({ files: valid.map(toPendingFileInfo) });

      // Upload each file
      const results: UploadedFileInfo[] = [];
      for (const entry of uploadingEntries) {
        try {
          const info = await uploadEntry(entry);
          results.push(info);
        } catch (err) {
          const message = err instanceof Error ? err.message : 'Upload failed';
          onUploadError?.({
            error: message,
            file: toPendingFileInfo(entry.file),
          });
        }
      }

      if (results.length > 0) {
        onUploadComplete?.({ files: results });
      }
    },
    [disabled, entries, multiple, validateFiles, uploadEntry, onSelect, onUploadStart, onUploadComplete, onUploadError],
  );

  // ── Remove a file ────────────────────────────────────────────────────────

  const handleRemove = useCallback(
    (entry: FileEntry) => {
      setEntries((prev) => prev.filter((e) => e.localId !== entry.localId));
      onRemove?.({ file: toPendingFileInfo(entry.file) });
    },
    [onRemove],
  );

  // ── Drag and drop ────────────────────────────────────────────────────────

  const handleDragOver = useCallback(
    (e: React.DragEvent) => {
      if (!dragDrop || disabled) return;
      e.preventDefault();
      e.stopPropagation();
      setIsDragOver(true);
    },
    [dragDrop, disabled],
  );

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragOver(false);
      if (!dragDrop || disabled) return;
      if (e.dataTransfer.files.length > 0) {
        void handleFiles(e.dataTransfer.files);
      }
    },
    [dragDrop, disabled, handleFiles],
  );

  const openFilePicker = useCallback(() => {
    if (!disabled) inputRef.current?.click();
  }, [disabled]);

  const handleInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      if (e.target.files && e.target.files.length > 0) {
        void handleFiles(e.target.files);
        // Reset input so the same file can be re-selected
        e.target.value = '';
      }
    },
    [handleFiles],
  );

  // ── Render ───────────────────────────────────────────────────────────────

  const displayError = localError ?? serverError;
  const completedEntries = entries.filter((e) => e.status === 'complete' && e.uploadedInfo?.id);

  return (
    <div className={cn('flex flex-col gap-2', className)} data-refast-id={dataRefastId}>
      {name && (
        multiple ? (
          completedEntries.map((entry) => (
            <input key={entry.uploadedInfo!.id} type="hidden" name={name} value={entry.uploadedInfo!.id} />
          ))
        ) : (
          completedEntries.length > 0 && (
            <input type="hidden" name={name} value={completedEntries[0].uploadedInfo!.id} />
          )
        )
      )}
      {/* Hidden file input */}
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        multiple={multiple}
        disabled={disabled}
        required={required}
        className="sr-only"
        aria-hidden="true"
        onChange={handleInputChange}
      />

      {/* Required label (dropzone variant shows it inside) */}
      {variant === 'button' && required && (
        <span className="text-xs text-muted-foreground">
          Required <span className="text-destructive">*</span>
        </span>
      )}

      {/* Drop zone or button */}
      {variant === 'dropzone' ? (
        <div
          role="button"
          tabIndex={disabled ? -1 : 0}
          aria-disabled={disabled}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault();
              openFilePicker();
            }
          }}
          onClick={openFilePicker}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={cn(
            'flex cursor-pointer flex-col items-center justify-center gap-2 rounded-lg border-2 border-dashed px-6 py-10 text-center transition-colors',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
            isDragOver && !disabled
              ? 'border-primary bg-primary/5'
              : 'border-border bg-muted/20 hover:border-primary/50 hover:bg-muted/40',
            disabled && 'cursor-not-allowed opacity-50',
            displayError && 'border-destructive',
          )}
        >
          <span className={cn('text-muted-foreground', isDragOver && 'text-primary')}>
            <Icon name={isDragOver ? 'download' : 'upload-cloud'} size={32} />
          </span>
          <div>
            <p className="font-medium text-foreground">
              {label}
              {required && <span className="ml-1 text-destructive">*</span>}
            </p>
            {description && (
              <p className="mt-0.5 text-sm text-muted-foreground">{description}</p>
            )}
            {dragDrop && (
              <p className="mt-1 text-xs text-muted-foreground">
                Drag &amp; drop or click to browse
              </p>
            )}
          </div>
          {(accept || maxSize || maxFiles) && (
            <p className="text-xs text-muted-foreground/70">
              {[
                accept && `Accepts: ${accept}`,
                maxSize && `Max size: ${formatBytes(maxSize)}`,
                maxFiles && `Max files: ${maxFiles}`,
              ]
                .filter(Boolean)
                .join(' · ')}
            </p>
          )}
        </div>
      ) : (
        <button
          type="button"
          disabled={disabled}
          onClick={openFilePicker}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={cn(
            'inline-flex items-center gap-2 rounded-md border border-input bg-background px-4 py-2 text-sm font-medium transition-colors',
            'hover:bg-accent hover:text-accent-foreground',
            'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2',
            'disabled:pointer-events-none disabled:opacity-50',
            isDragOver && 'border-primary bg-primary/5',
            displayError && 'border-destructive',
          )}
        >
          <Icon name="upload" size={16} />
          <span>
            {label}
            {required && <span className="ml-1 text-destructive">*</span>}
          </span>
        </button>
      )}

      {/* File list */}
      {entries.length > 0 && (
        <div className="flex flex-col gap-1.5">
          {entries.map((entry) => (
            <FileRow
              key={entry.localId}
              entry={entry}
              onRemove={() => handleRemove(entry)}
            />
          ))}
        </div>
      )}

      {/* Error message */}
      {displayError && (
        <p role="alert" className="flex items-center gap-1 text-sm text-destructive">
          <Icon name="alert-circle" size={14} />
          {displayError}
        </p>
      )}
    </div>
  );
};

FileUploader.displayName = 'FileUploader';
