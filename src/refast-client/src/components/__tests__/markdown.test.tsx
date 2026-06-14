import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Markdown } from '../shadcn/typography';
import { EventManagerProvider } from '../../events/EventManager';

describe('Markdown Component', () => {
  it('renders raw content or mock correctly', () => {
    const { container } = render(<Markdown content="Hello **world**" />);
    const pre = container.querySelector('pre');
    if (pre) {
      expect(pre).toHaveTextContent('Hello **world**');
    } else {
      const mockEl = screen.getByTestId('mocked-react-markdown');
      expect(mockEl).toBeInTheDocument();
    }
  });

  it('renders parsed rich markdown content after libraries load', async () => {
    render(<Markdown content="Hello **world**" />);
    const mockEl = await screen.findByTestId('mocked-react-markdown');
    expect(mockEl).toBeInTheDocument();
    expect(mockEl).toHaveTextContent('Hello **world**');
  });

  it('renders custom components using customComponents mapping', async () => {
    const customComponents = {
      'custom_btn_1': {
        type: 'Button',
        props: {},
        children: ['Test Button']
      }
    };
    
    const markdownContent = 'Click this button: ![Button](/refast-component/custom_btn_1)';
    
    render(
      <EventManagerProvider websocket={null}>
        <Markdown content={markdownContent} customComponents={customComponents} />
      </EventManagerProvider>
    );
    
    const button = await screen.findByRole('button', { name: /Test Button/i });
    expect(button).toBeInTheDocument();
  });
});

