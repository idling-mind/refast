import React from 'react';

interface SlotProps {
  id?: string;
  name?: string;
  fallback?: React.ReactNode;
  children?: React.ReactNode;
  'data-refast-id'?: string;
}

/**
 * Slot component - placeholder for dynamic content.
 */
export function Slot({
  id,
  name,
  fallback,
  children,
  'data-refast-id': dataRefastId,
}: SlotProps): React.ReactElement {
  return (
    <div id={id} data-slot-name={name} data-refast-id={dataRefastId}>
      {children || fallback || null}
    </div>
  );
}
