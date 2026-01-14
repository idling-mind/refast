import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import { Container, Text, Fragment } from '../base';
import { Button } from '../shadcn/button';
import { Card, CardHeader, CardContent, CardTitle } from '../shadcn/card';
import { Row, Column, Grid, Center } from '../shadcn/layout';
import { Input, Checkbox } from '../shadcn/input';
import { Heading, Paragraph, Link } from '../shadcn/typography';
import { Alert, Badge, Progress, Spinner } from '../shadcn/feedback';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, Avatar } from '../shadcn/data_display';

describe('Base Components', () => {
  it('renders Container', () => {
    render(<Container className="test-class">Content</Container>);
    expect(screen.getByText('Content')).toBeInTheDocument();
  });

  it('renders Text', () => {
    render(<Text>Hello World</Text>);
    expect(screen.getByText('Hello World')).toBeInTheDocument();
  });

  it('renders Fragment', () => {
    render(<Fragment><span>Child 1</span><span>Child 2</span></Fragment>);
    expect(screen.getByText('Child 1')).toBeInTheDocument();
    expect(screen.getByText('Child 2')).toBeInTheDocument();
  });
});

describe('Button Component', () => {
  it('renders button with text', () => {
    render(<Button>Click me</Button>);
    expect(screen.getByRole('button')).toHaveTextContent('Click me');
  });

  it('handles click events', () => {
    const onClick = vi.fn();
    render(<Button onClick={onClick}>Click</Button>);
    screen.getByRole('button').click();
    expect(onClick).toHaveBeenCalled();
  });

  it('can be disabled', () => {
    render(<Button disabled>Disabled</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('shows loading state', () => {
    render(<Button loading>Loading</Button>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});

describe('Card Components', () => {
  it('renders card structure', () => {
    render(
      <Card>
        <CardHeader>
          <CardTitle>Title</CardTitle>
        </CardHeader>
        <CardContent>Content</CardContent>
      </Card>
    );
    expect(screen.getByText('Title')).toBeInTheDocument();
    expect(screen.getByText('Content')).toBeInTheDocument();
  });
});

describe('Layout Components', () => {
  it('renders Row', () => {
    render(<Row>Row content</Row>);
    expect(screen.getByText('Row content')).toBeInTheDocument();
  });

  it('renders Column', () => {
    render(<Column>Column content</Column>);
    expect(screen.getByText('Column content')).toBeInTheDocument();
  });

  it('renders Grid', () => {
    render(<Grid columns={2}>Grid content</Grid>);
    expect(screen.getByText('Grid content')).toBeInTheDocument();
  });

  it('renders Center', () => {
    render(<Center>Centered</Center>);
    expect(screen.getByText('Centered')).toBeInTheDocument();
  });
});

describe('Input Components', () => {
  it('renders Input', () => {
    render(<Input placeholder="Enter text" />);
    expect(screen.getByPlaceholderText('Enter text')).toBeInTheDocument();
  });

  it('renders Checkbox with label', () => {
    render(<Checkbox label="Check me" />);
    expect(screen.getByText('Check me')).toBeInTheDocument();
  });
});

describe('Typography Components', () => {
  it('renders Heading', () => {
    render(<Heading level={1}>Main Title</Heading>);
    expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Main Title');
  });

  it('renders Paragraph', () => {
    render(<Paragraph>Some text</Paragraph>);
    expect(screen.getByText('Some text')).toBeInTheDocument();
  });

  it('renders Link', () => {
    render(<Link href="https://example.com">Click here</Link>);
    expect(screen.getByRole('link')).toHaveAttribute('href', 'https://example.com');
  });
});

describe('Feedback Components', () => {
  it('renders Alert', () => {
    render(<Alert>Alert message</Alert>);
    expect(screen.getByRole('alert')).toHaveTextContent('Alert message');
  });

  it('renders Badge', () => {
    render(<Badge>New</Badge>);
    expect(screen.getByText('New')).toBeInTheDocument();
  });

  it('renders Progress', () => {
    render(<Progress value={50} />);
    expect(screen.getByRole('progressbar')).toHaveAttribute('aria-valuenow', '50');
  });

  it('renders Spinner', () => {
    render(<Spinner />);
    expect(screen.getByRole('status')).toBeInTheDocument();
  });
});

describe('Data Display Components', () => {
  it('renders Table', () => {
    render(
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Header</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          <TableRow>
            <TableCell>Cell</TableCell>
          </TableRow>
        </TableBody>
      </Table>
    );
    expect(screen.getByRole('table')).toBeInTheDocument();
    expect(screen.getByText('Header')).toBeInTheDocument();
    expect(screen.getByText('Cell')).toBeInTheDocument();
  });

  it('renders Avatar with fallback', () => {
    render(<Avatar alt="John Doe" />);
    expect(screen.getByText('J')).toBeInTheDocument();
  });
});
