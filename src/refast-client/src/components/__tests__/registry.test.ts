import { describe, it, expect } from 'vitest';
import { componentRegistry } from '../registry';

describe('ComponentRegistry', () => {
  it('has base components registered', () => {
    expect(componentRegistry.has('Container')).toBe(true);
    expect(componentRegistry.has('Text')).toBe(true);
    expect(componentRegistry.has('Fragment')).toBe(true);
  });

  it('has layout components registered', () => {
    expect(componentRegistry.has('Row')).toBe(true);
    expect(componentRegistry.has('Column')).toBe(true);
    expect(componentRegistry.has('Grid')).toBe(true);
    expect(componentRegistry.has('Flex')).toBe(true);
    expect(componentRegistry.has('Center')).toBe(true);
  });

  it('has button components registered', () => {
    expect(componentRegistry.has('Button')).toBe(true);
    expect(componentRegistry.has('IconButton')).toBe(true);
  });

  it('has card components registered', () => {
    expect(componentRegistry.has('Card')).toBe(true);
    expect(componentRegistry.has('CardHeader')).toBe(true);
    expect(componentRegistry.has('CardContent')).toBe(true);
    expect(componentRegistry.has('CardFooter')).toBe(true);
    expect(componentRegistry.has('CardTitle')).toBe(true);
    expect(componentRegistry.has('CardDescription')).toBe(true);
  });

  it('has input components registered', () => {
    expect(componentRegistry.has('Input')).toBe(true);
    expect(componentRegistry.has('Textarea')).toBe(true);
    expect(componentRegistry.has('Select')).toBe(true);
    expect(componentRegistry.has('SelectOption')).toBe(true);
    expect(componentRegistry.has('Checkbox')).toBe(true);
    expect(componentRegistry.has('Radio')).toBe(true);
    expect(componentRegistry.has('RadioGroup')).toBe(true);
  });

  it('has typography components registered', () => {
    expect(componentRegistry.has('Heading')).toBe(true);
    expect(componentRegistry.has('Paragraph')).toBe(true);
    expect(componentRegistry.has('Link')).toBe(true);
    expect(componentRegistry.has('Code')).toBe(true);
    expect(componentRegistry.has('BlockQuote')).toBe(true);
    expect(componentRegistry.has('List')).toBe(true);
    expect(componentRegistry.has('ListItem')).toBe(true);
    expect(componentRegistry.has('Label')).toBe(true);
  });

  it('has feedback components registered', () => {
    expect(componentRegistry.has('Alert')).toBe(true);
    expect(componentRegistry.has('AlertTitle')).toBe(true);
    expect(componentRegistry.has('AlertDescription')).toBe(true);
    expect(componentRegistry.has('Badge')).toBe(true);
    expect(componentRegistry.has('Progress')).toBe(true);
    expect(componentRegistry.has('Spinner')).toBe(true);
    expect(componentRegistry.has('Toast')).toBe(true);
    expect(componentRegistry.has('Skeleton')).toBe(true);
  });

  it('has data display components registered', () => {
    expect(componentRegistry.has('Table')).toBe(true);
    expect(componentRegistry.has('TableHeader')).toBe(true);
    expect(componentRegistry.has('TableBody')).toBe(true);
    expect(componentRegistry.has('TableRow')).toBe(true);
    expect(componentRegistry.has('TableHead')).toBe(true);
    expect(componentRegistry.has('TableCell')).toBe(true);
    expect(componentRegistry.has('Avatar')).toBe(true);
    expect(componentRegistry.has('Image')).toBe(true);
    expect(componentRegistry.has('Tooltip')).toBe(true);
  });

  it('has slot component registered', () => {
    expect(componentRegistry.has('Slot')).toBe(true);
  });

  it('returns undefined for unknown components', () => {
    expect(componentRegistry.get('Unknown')).toBeUndefined();
  });

  it('lists all registered components', () => {
    const list = componentRegistry.list();
    expect(list.length).toBeGreaterThan(40);
    expect(list).toContain('Container');
    expect(list).toContain('Button');
  });
});
