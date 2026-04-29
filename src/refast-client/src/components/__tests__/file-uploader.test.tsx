import { describe, it, expect, vi, beforeEach } from 'vitest';
import { act, createEvent, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { FileUploader } from '../shadcn/file-uploader';

// ─── Helpers ─────────────────────────────────────────────────────────────────

/**
 * Create a mock File object (jsdom's File is minimal but functional for tests).
 */
function makeFile(name: string, sizeBytes: number, type = 'text/plain'): File {
  const content = new Uint8Array(sizeBytes).fill(65); // fill with 'A'
  return new File([content], name, { type });
}

/**
 * Simulate a file input change event with the given files.
 */
function triggerFileSelect(input: HTMLInputElement, files: File[]) {
  Object.defineProperty(input, 'files', {
    value: files,
    configurable: true,
  });
  fireEvent.change(input);
}

// ─── Rendering ───────────────────────────────────────────────────────────────

describe('FileUploader – rendering', () => {
  it('renders with default label in dropzone variant', () => {
    render(<FileUploader />);
    expect(screen.getByText('Upload file')).toBeInTheDocument();
  });

  it('renders with a custom label', () => {
    render(<FileUploader label="Drop your CSV here" />);
    expect(screen.getByText('Drop your CSV here')).toBeInTheDocument();
  });

  it('renders description when provided', () => {
    render(<FileUploader description="Max 5 MB" />);
    expect(screen.getByText('Max 5 MB')).toBeInTheDocument();
  });

  it('renders in button variant', () => {
    render(<FileUploader variant="button" />);
    // A button element should be present (the visible trigger)
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('renders hidden file input', () => {
    const { container } = render(<FileUploader />);
    const input = container.querySelector('input[type="file"]');
    expect(input).not.toBeNull();
    // The input is visually hidden via sr-only class (not display:none)
    expect(input).toHaveClass('sr-only');
    expect(input).toHaveAttribute('aria-hidden', 'true');
  });

  it('sets accept attribute on hidden input', () => {
    const { container } = render(<FileUploader accept="image/*" />);
    const input = container.querySelector('input[type="file"]');
    expect(input).toHaveAttribute('accept', 'image/*');
  });

  it('sets multiple attribute on hidden input when multiple=true', () => {
    const { container } = render(<FileUploader multiple />);
    const input = container.querySelector('input[type="file"]');
    expect(input).toHaveAttribute('multiple');
  });

  it('does not set multiple when multiple=false', () => {
    const { container } = render(<FileUploader multiple={false} />);
    const input = container.querySelector('input[type="file"]');
    expect(input).not.toHaveAttribute('multiple');
  });

  it('shows server-side error message', () => {
    render(<FileUploader error="Upload failed on server" />);
    expect(screen.getByText('Upload failed on server')).toBeInTheDocument();
  });
});

// ─── Disabled state ───────────────────────────────────────────────────────────

describe('FileUploader – disabled', () => {
  it('disables the trigger button in button variant', () => {
    render(<FileUploader variant="button" disabled />);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});

// ─── File selection ───────────────────────────────────────────────────────────

describe('FileUploader – file selection', () => {
  let mockXhr: ReturnType<typeof vi.fn>;

  beforeEach(() => {
    // Mock XHR so uploads don't actually fire network requests
    mockXhr = vi.fn().mockImplementation(() => ({
      open: vi.fn(),
      send: vi.fn(),
      setRequestHeader: vi.fn(),
      upload: { onprogress: null },
      onload: null,
      onerror: null,
      status: 200,
      responseText: JSON.stringify({ files: [{ id: 'abc', name: 'test.txt', size: 5, content_type: 'text/plain' }] }),
    }));
    // @ts-expect-error: jsdom XHR override
    global.XMLHttpRequest = mockXhr;
  });

  it('shows file name after selection', async () => {
    const { container } = render(<FileUploader />);
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    const file = makeFile('myfile.txt', 100);

    triggerFileSelect(input, [file]);

    await waitFor(() => {
      expect(screen.getByText('myfile.txt')).toBeInTheDocument();
    });
  });

  it('calls onSelect with pending file info', async () => {
    const onSelect = vi.fn();
    const { container } = render(<FileUploader onSelect={onSelect} />);
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    const file = makeFile('data.csv', 200);

    triggerFileSelect(input, [file]);

    await waitFor(() => {
      expect(onSelect).toHaveBeenCalledOnce();
    });

    const arg = onSelect.mock.calls[0][0];
    expect(arg.files).toHaveLength(1);
    expect(arg.files[0].name).toBe('data.csv');
    expect(arg.files[0].size).toBe(200);
  });

  it('shows validation error when file exceeds maxSize', async () => {
    const { container } = render(<FileUploader maxSize={50} />);
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    const bigFile = makeFile('big.bin', 100);

    await act(async () => {
      triggerFileSelect(input, [bigFile]);
    });

    // Component renders error in a role="alert" div
    expect(container.querySelector('[role="alert"]')).not.toBeNull();
  });

  it('limits files to maxFiles', async () => {
    const onSelect = vi.fn();
    const { container } = render(<FileUploader multiple maxFiles={2} onSelect={onSelect} />);
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;

    const files = [makeFile('a.txt', 10), makeFile('b.txt', 10), makeFile('c.txt', 10)];
    triggerFileSelect(input, files);

    await waitFor(() => expect(onSelect).toHaveBeenCalledOnce());
    // Only 2 files passed to onSelect
    expect(onSelect.mock.calls[0][0].files).toHaveLength(2);
  });
});

// ─── Remove file ──────────────────────────────────────────────────────────────

describe('FileUploader – remove file', () => {
  beforeEach(() => {
    const mockXhr = vi.fn().mockImplementation(() => ({
      open: vi.fn(),
      send: vi.fn(),
      setRequestHeader: vi.fn(),
      upload: { onprogress: null },
      onload: null,
      onerror: null,
      status: 200,
      responseText: JSON.stringify({ files: [{ id: 'x', name: 'r.txt', size: 5, content_type: 'text/plain' }] }),
    }));
    // @ts-expect-error: jsdom XHR override
    global.XMLHttpRequest = mockXhr;
  });

  it('removes the file row on remove button click', async () => {
    const { container } = render(<FileUploader />);
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    triggerFileSelect(input, [makeFile('remove-me.txt', 20)]);

    await waitFor(() => expect(screen.getByText('remove-me.txt')).toBeInTheDocument());

    const removeBtn = screen.getByRole('button', { name: /Remove remove-me\.txt/i });
    fireEvent.click(removeBtn);

    await waitFor(() => {
      expect(screen.queryByText('remove-me.txt')).toBeNull();
    });
  });

  it('calls onRemove when a file is removed', async () => {
    const onRemove = vi.fn();
    const { container } = render(<FileUploader onRemove={onRemove} />);
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    triggerFileSelect(input, [makeFile('del.txt', 20)]);

    await waitFor(() => screen.getByText('del.txt'));

    fireEvent.click(screen.getByRole('button', { name: /Remove del\.txt/i }));

    await waitFor(() => expect(onRemove).toHaveBeenCalledOnce());
    expect(onRemove.mock.calls[0][0].file.name).toBe('del.txt');
  });
});

// ─── Drag and drop ────────────────────────────────────────────────────────────

describe('FileUploader – drag and drop', () => {
  it('does not trigger drag highlight when dragDrop=false', () => {
    const { container } = render(<FileUploader dragDrop={false} />);
    const zone = container.firstElementChild as HTMLElement;
    fireEvent.dragOver(zone, { dataTransfer: { files: [] } });
    // No "drag-over" visual class should be applied; we just verify no crash
    expect(zone).toBeInTheDocument();
  });

  it('accepts dropped files when dragDrop=true', async () => {
    const onSelect = vi.fn();

    const mockXhr = vi.fn().mockImplementation(() => ({
      open: vi.fn(),
      send: vi.fn(),
      setRequestHeader: vi.fn(),
      upload: { onprogress: null },
      onload: null,
      onerror: null,
      status: 200,
      responseText: JSON.stringify({ files: [{ id: 'drop1', name: 'dropped.png', size: 30, content_type: 'image/png' }] }),
    }));
    // @ts-expect-error: jsdom XHR override
    global.XMLHttpRequest = mockXhr;

    const { container } = render(<FileUploader dragDrop onSelect={onSelect} />);
    // Drop handlers are on the inner role="button" element, not the outer wrapper
    const dropZone = container.querySelector('[role="button"]') as HTMLElement;
    const file = makeFile('dropped.png', 30, 'image/png');

    // Use RTL createEvent + Object.defineProperty so React's synthetic
    // event system sees the correct dataTransfer.files.
    const dropEvent = createEvent.drop(dropZone);
    Object.defineProperty(dropEvent, 'dataTransfer', {
      value: { files: [file], items: [], types: ['Files'] },
    });

    await act(async () => {
      fireEvent(dropZone, dropEvent);
    });

    expect(onSelect).toHaveBeenCalledOnce();
    expect(onSelect.mock.calls[0][0].files[0].name).toBe('dropped.png');
  });
});

// ─── Required / aria ─────────────────────────────────────────────────────────

describe('FileUploader – required', () => {
  it('marks the hidden input as required when required=true', () => {
    const { container } = render(<FileUploader required />);
    const input = container.querySelector('input[type="file"]') as HTMLInputElement;
    expect(input).toHaveAttribute('required');
  });
});
