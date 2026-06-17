import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen } from '@testing-library/react';
import { ComponentRenderer } from '../ComponentRenderer';

vi.mock('../../events/EventManager', () => ({
  useEventManager: () => ({
    invokeCallback: vi.fn(),
    emitEvent: vi.fn(),
    subscribe: vi.fn(),
    unsubscribe: vi.fn(),
    onUpdate: vi.fn(() => vi.fn()),
    registerMessageHandler: vi.fn(() => vi.fn()),
    websocket: null,
  })
}));

describe('ComponentRenderer - Unknown components', () => {
  const unknownTree = {
    type: 'NonExistentSuperWidget',
    id: 'missing_widget_id',
    props: { title: 'Unsupported Widget' },
  };

  beforeEach(() => {
    vi.stubGlobal('__REFAST_DEBUG__', undefined);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it('renders nothing (null) when debug is false', () => {
    window.__REFAST_DEBUG__ = false;
    const { container } = render(<ComponentRenderer tree={unknownTree} />);
    expect(container.firstChild).toBeNull();
  });

  it('renders nothing (null) when debug is undefined/falsy', () => {
    const { container } = render(<ComponentRenderer tree={unknownTree} />);
    expect(container.firstChild).toBeNull();
  });

  it('renders inline popover trigger when debug is true', () => {
    window.__REFAST_DEBUG__ = true;
    render(<ComponentRenderer tree={unknownTree} />);
    
    const trigger = screen.getByText('Unknown: NonExistentSuperWidget');
    expect(trigger).toBeInTheDocument();
    expect(trigger).toHaveAttribute('data-unknown-type', 'NonExistentSuperWidget');
  });
});
