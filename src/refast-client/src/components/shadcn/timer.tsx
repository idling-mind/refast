/**
 * Timer — an invisible component that fires a server callback at a regular
 * interval.  Renders nothing in the DOM.
 */

import { useEffect, useRef } from 'react';

export interface TimerProps {
  /** Milliseconds between ticks (>= 100). */
  interval?: number;
  /** When false the timer is paused. */
  enabled?: boolean;
  /** Callback fired on each tick. Resolved from a server Callback action ref. */
  onTick?: () => void;
}

export function Timer({ interval = 1000, enabled = true, onTick }: TimerProps) {
  // Keep a stable ref to the latest onTick so the interval closure never
  // captures a stale version.
  const onTickRef = useRef(onTick);
  useEffect(() => {
    onTickRef.current = onTick;
  });

  useEffect(() => {
    if (!enabled || !onTick) return;

    const id = setInterval(() => {
      onTickRef.current?.();
    }, interval);

    return () => clearInterval(id);
  }, [enabled, interval, onTick]);

  return null;
}
