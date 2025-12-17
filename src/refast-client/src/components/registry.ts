import React from 'react';

// Import base components
import { Container, Text, Fragment } from './base';

// Import shadcn components
import { Row, Column, Stack, Grid, Flex, Center, Spacer, Divider } from './shadcn/layout';
import { Button, IconButton } from './shadcn/button';
import { Card, CardHeader, CardContent, CardFooter, CardTitle, CardDescription } from './shadcn/card';
import { Input, Textarea, Select, SelectOption, Checkbox, Radio, RadioGroup } from './shadcn/input';
import { Slot } from './shadcn/slot';
import { Heading, Paragraph, Link, Code, BlockQuote, List, ListItem, Label } from './shadcn/typography';
import { Alert, AlertTitle, AlertDescription, Badge, Progress, Spinner, Toast, Skeleton } from './shadcn/feedback';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, Avatar, Image, Tooltip } from './shadcn/data_display';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type ComponentType = React.ComponentType<any>;

/**
 * Registry of all available components.
 */
class ComponentRegistry {
  private components: Map<string, ComponentType> = new Map();

  register(name: string, component: ComponentType): void {
    this.components.set(name, component);
  }

  get(name: string): ComponentType | undefined {
    return this.components.get(name);
  }

  has(name: string): boolean {
    return this.components.has(name);
  }

  list(): string[] {
    return Array.from(this.components.keys());
  }

  /**
   * Register multiple components at once.
   */
  registerAll(components: Record<string, ComponentType>): void {
    for (const [name, component] of Object.entries(components)) {
      this.register(name, component);
    }
  }
}

export const componentRegistry = new ComponentRegistry();

// Register base components
componentRegistry.register('Container', Container);
componentRegistry.register('Text', Text);
componentRegistry.register('Fragment', Fragment);

// Register slot component
componentRegistry.register('Slot', Slot);

// Register layout components
componentRegistry.register('Row', Row);
componentRegistry.register('Column', Column);
componentRegistry.register('Stack', Stack);
componentRegistry.register('Grid', Grid);
componentRegistry.register('Flex', Flex);
componentRegistry.register('Center', Center);
componentRegistry.register('Spacer', Spacer);
componentRegistry.register('Divider', Divider);

// Register button components
componentRegistry.register('Button', Button);
componentRegistry.register('IconButton', IconButton);

// Register card components
componentRegistry.register('Card', Card);
componentRegistry.register('CardHeader', CardHeader);
componentRegistry.register('CardContent', CardContent);
componentRegistry.register('CardFooter', CardFooter);
componentRegistry.register('CardTitle', CardTitle);
componentRegistry.register('CardDescription', CardDescription);

// Register input components
componentRegistry.register('Input', Input);
componentRegistry.register('Textarea', Textarea);
componentRegistry.register('Select', Select);
componentRegistry.register('SelectOption', SelectOption);
componentRegistry.register('Checkbox', Checkbox);
componentRegistry.register('Radio', Radio);
componentRegistry.register('RadioGroup', RadioGroup);

// Register typography components
componentRegistry.register('Heading', Heading);
componentRegistry.register('Paragraph', Paragraph);
componentRegistry.register('Link', Link);
componentRegistry.register('Code', Code);
componentRegistry.register('BlockQuote', BlockQuote);
componentRegistry.register('List', List);
componentRegistry.register('ListItem', ListItem);
componentRegistry.register('Label', Label);

// Register feedback components
componentRegistry.register('Alert', Alert);
componentRegistry.register('AlertTitle', AlertTitle);
componentRegistry.register('AlertDescription', AlertDescription);
componentRegistry.register('Badge', Badge);
componentRegistry.register('Progress', Progress);
componentRegistry.register('Spinner', Spinner);
componentRegistry.register('Toast', Toast);
componentRegistry.register('Skeleton', Skeleton);

// Register data display components
componentRegistry.register('Table', Table);
componentRegistry.register('TableHeader', TableHeader);
componentRegistry.register('TableBody', TableBody);
componentRegistry.register('TableRow', TableRow);
componentRegistry.register('TableHead', TableHead);
componentRegistry.register('TableCell', TableCell);
componentRegistry.register('Avatar', Avatar);
componentRegistry.register('Image', Image);
componentRegistry.register('Tooltip', Tooltip);
