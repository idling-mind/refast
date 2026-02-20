import React from 'react';

// ── Eager imports: core components that are always loaded ──────────────────

// Import base components
import { Container, Text, Fragment } from './base';

// Import shadcn components (core set – always loaded)
import { Row, Column, Grid, Flex, Center } from './shadcn/layout';
import { Button, IconButton } from './shadcn/button';
import { Card, CardHeader, CardContent, CardFooter, CardTitle, CardDescription } from './shadcn/card';
import { Input, InputWrapper, Textarea, Select, SelectOption, Checkbox, Radio, RadioGroup, CheckboxGroup } from './shadcn/input';
import { Slot } from './shadcn/slot';
import { Heading, Paragraph, Link, Code, BlockQuote, List, ListItem, Label, Markdown } from './shadcn/typography';
import { Alert, AlertTitle, AlertDescription, Badge, Progress, Spinner, Skeleton } from './shadcn/feedback';
import { ConnectionStatus } from './shadcn/ConnectionStatus';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, DataTable, Avatar, Image, Tooltip, Tabs, TabItem, Accordion, AccordionItem, AccordionTrigger, AccordionContent } from './shadcn/data_display';

// Import utility components that are lightweight
import {
  Toaster, Separator, AspectRatio, ScrollArea, Collapsible, CollapsibleTrigger, CollapsibleContent,
  Carousel, CarouselContent, CarouselItem, CarouselPrevious, CarouselNext,
  ResizablePanelGroup, ResizablePanel, ResizableHandle, ThemeSwitcher
} from './shadcn/utility';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type ComponentType = React.ComponentType<any>;

/**
 * A lazy component loader: a function that returns a promise resolving to
 * a record of component names → React components.
 */
export type LazyChunkLoader = () => Promise<Record<string, ComponentType>>;

/**
 * Describes a feature chunk that can be lazily loaded.
 */
export interface FeatureChunk {
  /** Human-readable chunk name (e.g., "charts", "navigation") */
  name: string;
  /** Component names that belong to this chunk */
  componentNames: string[];
  /** Loader function that dynamically imports the chunk */
  loader: LazyChunkLoader;
}

/**
 * Registry of all available components.
 *
 * Supports two registration modes:
 * - **Eager**: component reference stored directly (core components)
 * - **Lazy**: a chunk loader is stored; the component is resolved on first
 *   access via `React.lazy()` + `<Suspense>`.
 *
 * Extensions continue to use `register()` / `registerAll()` exactly as before.
 */
class ComponentRegistry {
  private components: Map<string, ComponentType> = new Map();
  /** Maps component name → the chunk it belongs to (for lazy resolution) */
  private lazyMap: Map<string, string> = new Map();
  /** Registered chunk loaders */
  private chunkLoaders: Map<string, LazyChunkLoader> = new Map();
  /** Cache of resolved lazy components (wrapped in React.lazy) */
  private lazyCache: Map<string, ComponentType> = new Map();
  /** Chunk load promises (so we don't trigger the same import twice) */
  private chunkPromises: Map<string, Promise<Record<string, ComponentType>>> = new Map();
  /** Which chunks have been fully resolved */
  private resolvedChunks: Set<string> = new Set();

  // ── Eager registration (unchanged API) ─────────────────────────────

  register(name: string, component: ComponentType): void {
    this.components.set(name, component);
  }

  registerAll(components: Record<string, ComponentType>): void {
    for (const [name, component] of Object.entries(components)) {
      this.register(name, component);
    }
  }

  // ── Lazy registration ──────────────────────────────────────────────

  /**
   * Register a feature chunk whose components will be lazily loaded.
   */
  registerLazyChunk(chunk: FeatureChunk): void {
    this.chunkLoaders.set(chunk.name, chunk.loader);
    for (const name of chunk.componentNames) {
      this.lazyMap.set(name, chunk.name);
    }
  }

  // ── Component resolution ───────────────────────────────────────────

  /**
   * Get a component by name.
   *
   * 1. If eagerly registered → return immediately.
   * 2. If the component belongs to a lazy chunk → return a `React.lazy()`
   *    wrapper that will trigger the chunk import on first render.
   * 3. Otherwise → return `undefined`.
   */
  get(name: string): ComponentType | undefined {
    // 1. Eager
    const eager = this.components.get(name);
    if (eager) return eager;

    // 2. Lazy
    const chunkName = this.lazyMap.get(name);
    if (!chunkName) return undefined;

    // If the chunk has already been fully resolved, check the eager map
    // (resolved components are promoted to eager after loading)
    if (this.resolvedChunks.has(chunkName)) {
      return this.components.get(name);
    }

    // Return a cached React.lazy wrapper (create one if it doesn't exist)
    let lazy = this.lazyCache.get(name);
    if (!lazy) {
      lazy = React.lazy(() => this._loadComponent(name, chunkName));
      this.lazyCache.set(name, lazy);
    }
    return lazy;
  }

  has(name: string): boolean {
    return this.components.has(name) || this.lazyMap.has(name);
  }

  /**
   * Check whether a component name is registered as part of a lazy chunk
   * that hasn't been loaded yet.
   */
  isLazy(name: string): boolean {
    if (this.components.has(name)) return false;
    const chunkName = this.lazyMap.get(name);
    if (!chunkName) return false;
    return !this.resolvedChunks.has(chunkName);
  }

  list(): string[] {
    const all = new Set([...this.components.keys(), ...this.lazyMap.keys()]);
    return Array.from(all);
  }

  /**
   * List all registered feature-chunk names.
   */
  listChunks(): string[] {
    return Array.from(this.chunkLoaders.keys());
  }

  // ── Internal ───────────────────────────────────────────────────────

  /**
   * Load a single component from its chunk.  Returns in the shape
   * `{ default: Component }` which `React.lazy()` requires.
   */
  private async _loadComponent(
    name: string,
    chunkName: string,
  ): Promise<{ default: ComponentType }> {
    // De-duplicate chunk loading
    let promise = this.chunkPromises.get(chunkName);
    if (!promise) {
      const loader = this.chunkLoaders.get(chunkName);
      if (!loader) throw new Error(`No loader for chunk "${chunkName}"`);
      promise = loader();
      this.chunkPromises.set(chunkName, promise);
    }

    const exports = await promise;

    // Promote all resolved components to eager so subsequent `get()` calls
    // skip the lazy path entirely.
    for (const [n, comp] of Object.entries(exports)) {
      this.components.set(n, comp);
    }
    this.resolvedChunks.add(chunkName);

    const component = exports[name];
    if (!component) {
      throw new Error(
        `Component "${name}" not found in chunk "${chunkName}". ` +
        `Available: ${Object.keys(exports).join(', ')}`,
      );
    }
    return { default: component };
  }
}

export const componentRegistry = new ComponentRegistry();

// ═══════════════════════════════════════════════════════════════════════════
// Register core (always-loaded) components
// ═══════════════════════════════════════════════════════════════════════════

// Base
componentRegistry.register('Container', Container);
componentRegistry.register('Text', Text);
componentRegistry.register('Fragment', Fragment);

// Slot
componentRegistry.register('Slot', Slot);

// Layout
componentRegistry.register('Row', Row);
componentRegistry.register('Column', Column);
componentRegistry.register('Grid', Grid);
componentRegistry.register('Flex', Flex);
componentRegistry.register('Center', Center);

// Button
componentRegistry.register('Button', Button);
componentRegistry.register('IconButton', IconButton);

// Card
componentRegistry.register('Card', Card);
componentRegistry.register('CardHeader', CardHeader);
componentRegistry.register('CardContent', CardContent);
componentRegistry.register('CardFooter', CardFooter);
componentRegistry.register('CardTitle', CardTitle);
componentRegistry.register('CardDescription', CardDescription);

// Input
componentRegistry.register('Input', Input);
componentRegistry.register('InputWrapper', InputWrapper);
componentRegistry.register('Textarea', Textarea);
componentRegistry.register('Select', Select);
componentRegistry.register('SelectOption', SelectOption);
componentRegistry.register('Checkbox', Checkbox);
componentRegistry.register('CheckboxGroup', CheckboxGroup);
componentRegistry.register('Radio', Radio);
componentRegistry.register('RadioGroup', RadioGroup);

// Typography
componentRegistry.register('Heading', Heading);
componentRegistry.register('Paragraph', Paragraph);
componentRegistry.register('Link', Link);
componentRegistry.register('Code', Code);
componentRegistry.register('BlockQuote', BlockQuote);
componentRegistry.register('List', List);
componentRegistry.register('ListItem', ListItem);
componentRegistry.register('Label', Label);
componentRegistry.register('Markdown', Markdown);

// Feedback
componentRegistry.register('Alert', Alert);
componentRegistry.register('AlertTitle', AlertTitle);
componentRegistry.register('AlertDescription', AlertDescription);
componentRegistry.register('Badge', Badge);
componentRegistry.register('Progress', Progress);
componentRegistry.register('Spinner', Spinner);
componentRegistry.register('Toast', Toaster);
componentRegistry.register('Skeleton', Skeleton);
componentRegistry.register('ConnectionStatus', ConnectionStatus);

// Data display
componentRegistry.register('Table', Table);
componentRegistry.register('TableHeader', TableHeader);
componentRegistry.register('TableBody', TableBody);
componentRegistry.register('TableRow', TableRow);
componentRegistry.register('TableHead', TableHead);
componentRegistry.register('TableCell', TableCell);
componentRegistry.register('DataTable', DataTable);
componentRegistry.register('Avatar', Avatar);
componentRegistry.register('Image', Image);
componentRegistry.register('Tooltip', Tooltip);
componentRegistry.register('Tabs', Tabs);
componentRegistry.register('TabItem', TabItem);
componentRegistry.register('Accordion', Accordion);
componentRegistry.register('AccordionItem', AccordionItem);
componentRegistry.register('AccordionTrigger', AccordionTrigger);
componentRegistry.register('AccordionContent', AccordionContent);

// Utility
componentRegistry.register('Separator', Separator);
componentRegistry.register('AspectRatio', AspectRatio);
componentRegistry.register('ScrollArea', ScrollArea);
componentRegistry.register('Collapsible', Collapsible);
componentRegistry.register('CollapsibleTrigger', CollapsibleTrigger);
componentRegistry.register('CollapsibleContent', CollapsibleContent);
componentRegistry.register('Carousel', Carousel);
componentRegistry.register('CarouselContent', CarouselContent);
componentRegistry.register('CarouselItem', CarouselItem);
componentRegistry.register('CarouselPrevious', CarouselPrevious);
componentRegistry.register('CarouselNext', CarouselNext);
componentRegistry.register('ResizablePanelGroup', ResizablePanelGroup);
componentRegistry.register('ResizablePanel', ResizablePanel);
componentRegistry.register('ResizableHandle', ResizableHandle);
componentRegistry.register('ThemeSwitcher', ThemeSwitcher);

// ═══════════════════════════════════════════════════════════════════════════
// Register lazy feature chunks
// ═══════════════════════════════════════════════════════════════════════════

componentRegistry.registerLazyChunk({
  name: 'icons',
  componentNames: ['Icon'],
  loader: () =>
    import('./shadcn/icon').then((m) => ({ Icon: m.Icon })),
});

componentRegistry.registerLazyChunk({
  name: 'controls',
  componentNames: [
    'Switch', 'Slider', 'Toggle', 'ToggleGroup', 'ToggleGroupItem',
    'DatePicker', 'Calendar', 'Combobox',
    'InputOTP', 'InputOTPGroup', 'InputOTPSlot', 'InputOTPSeparator',
  ],
  loader: () =>
    import('./shadcn/controls').then((m) => ({
      Switch: m.Switch, Slider: m.Slider, Toggle: m.Toggle,
      ToggleGroup: m.ToggleGroup, ToggleGroupItem: m.ToggleGroupItem,
      DatePicker: m.DatePicker, Calendar: m.Calendar, Combobox: m.Combobox,
      InputOTP: m.InputOTP, InputOTPGroup: m.InputOTPGroup,
      InputOTPSlot: m.InputOTPSlot, InputOTPSeparator: m.InputOTPSeparator,
    })),
});

componentRegistry.registerLazyChunk({
  name: 'navigation',
  componentNames: [
    'Breadcrumb', 'BreadcrumbList', 'BreadcrumbItem', 'BreadcrumbLink',
    'BreadcrumbPage', 'BreadcrumbSeparator', 'BreadcrumbEllipsis',
    'NavigationMenu', 'NavigationMenuList', 'NavigationMenuItem',
    'NavigationMenuTrigger', 'NavigationMenuContent', 'NavigationMenuLink',
    'Pagination', 'PaginationContent', 'PaginationItem', 'PaginationLink',
    'PaginationPrevious', 'PaginationNext', 'PaginationEllipsis',
    'Menubar', 'MenubarMenu', 'MenubarTrigger', 'MenubarContent',
    'MenubarItem', 'MenubarSeparator', 'MenubarCheckboxItem',
    'MenubarRadioGroup', 'MenubarRadioItem', 'MenubarSub',
    'MenubarSubTrigger', 'MenubarSubContent',
    'Command', 'CommandInput', 'CommandList', 'CommandEmpty',
    'CommandGroup', 'CommandItem', 'CommandSeparator', 'CommandShortcut',
    'SidebarProvider', 'Sidebar', 'SidebarInset', 'SidebarHeader',
    'SidebarContent', 'SidebarFooter', 'SidebarSeparator',
    'SidebarGroup', 'SidebarGroupLabel', 'SidebarGroupAction',
    'SidebarGroupContent',
    'SidebarMenu', 'SidebarMenuItem', 'SidebarMenuButton',
    'SidebarMenuAction', 'SidebarMenuBadge',
    'SidebarMenuSub', 'SidebarMenuSubItem', 'SidebarMenuSubButton',
    'SidebarMenuSkeleton',
    'SidebarRail', 'SidebarTrigger',
  ],
  loader: () =>
    import('./shadcn/navigation').then((m) => ({
      Breadcrumb: m.Breadcrumb, BreadcrumbList: m.BreadcrumbList,
      BreadcrumbItem: m.BreadcrumbItem, BreadcrumbLink: m.BreadcrumbLink,
      BreadcrumbPage: m.BreadcrumbPage, BreadcrumbSeparator: m.BreadcrumbSeparator,
      BreadcrumbEllipsis: m.BreadcrumbEllipsis,
      NavigationMenu: m.NavigationMenu, NavigationMenuList: m.NavigationMenuList,
      NavigationMenuItem: m.NavigationMenuItem, NavigationMenuTrigger: m.NavigationMenuTrigger,
      NavigationMenuContent: m.NavigationMenuContent, NavigationMenuLink: m.NavigationMenuLink,
      Pagination: m.Pagination, PaginationContent: m.PaginationContent,
      PaginationItem: m.PaginationItem, PaginationLink: m.PaginationLink,
      PaginationPrevious: m.PaginationPrevious, PaginationNext: m.PaginationNext,
      PaginationEllipsis: m.PaginationEllipsis,
      Menubar: m.Menubar, MenubarMenu: m.MenubarMenu, MenubarTrigger: m.MenubarTrigger,
      MenubarContent: m.MenubarContent, MenubarItem: m.MenubarItem,
      MenubarSeparator: m.MenubarSeparator, MenubarCheckboxItem: m.MenubarCheckboxItem,
      MenubarRadioGroup: m.MenubarRadioGroup, MenubarRadioItem: m.MenubarRadioItem,
      MenubarSub: m.MenubarSub, MenubarSubTrigger: m.MenubarSubTrigger,
      MenubarSubContent: m.MenubarSubContent,
      Command: m.Command, CommandInput: m.CommandInput, CommandList: m.CommandList,
      CommandEmpty: m.CommandEmpty, CommandGroup: m.CommandGroup,
      CommandItem: m.CommandItem, CommandSeparator: m.CommandSeparator,
      CommandShortcut: m.CommandShortcut,
      SidebarProvider: m.SidebarProvider, Sidebar: m.Sidebar, SidebarInset: m.SidebarInset,
      SidebarHeader: m.SidebarHeader, SidebarContent: m.SidebarContent,
      SidebarFooter: m.SidebarFooter, SidebarSeparator: m.SidebarSeparator,
      SidebarGroup: m.SidebarGroup, SidebarGroupLabel: m.SidebarGroupLabel,
      SidebarGroupAction: m.SidebarGroupAction, SidebarGroupContent: m.SidebarGroupContent,
      SidebarMenu: m.SidebarMenu, SidebarMenuItem: m.SidebarMenuItem,
      SidebarMenuButton: m.SidebarMenuButton, SidebarMenuAction: m.SidebarMenuAction,
      SidebarMenuBadge: m.SidebarMenuBadge,
      SidebarMenuSub: m.SidebarMenuSub, SidebarMenuSubItem: m.SidebarMenuSubItem,
      SidebarMenuSubButton: m.SidebarMenuSubButton, SidebarMenuSkeleton: m.SidebarMenuSkeleton,
      SidebarRail: m.SidebarRail, SidebarTrigger: m.SidebarTrigger,
    })),
});

componentRegistry.registerLazyChunk({
  name: 'overlay',
  componentNames: [
    'Dialog', 'DialogTrigger', 'DialogContent', 'DialogHeader', 'DialogFooter',
    'DialogTitle', 'DialogDescription', 'DialogAction', 'DialogCancel',
    'Drawer', 'DrawerTrigger', 'DrawerContent', 'DrawerHeader', 'DrawerFooter',
    'DrawerTitle', 'DrawerDescription', 'DrawerClose',
    'Sheet', 'SheetTrigger', 'SheetContent', 'SheetHeader', 'SheetFooter',
    'SheetTitle', 'SheetDescription', 'SheetClose',
    'HoverCard', 'HoverCardTrigger', 'HoverCardContent',
    'Popover', 'PopoverTrigger', 'PopoverContent',
    'DropdownMenu', 'DropdownMenuTrigger', 'DropdownMenuContent',
    'DropdownMenuItem', 'DropdownMenuLabel', 'DropdownMenuSeparator',
    'DropdownMenuCheckboxItem', 'DropdownMenuRadioGroup', 'DropdownMenuRadioItem',
    'DropdownMenuSub', 'DropdownMenuSubTrigger', 'DropdownMenuSubContent',
    'ContextMenu', 'ContextMenuTrigger', 'ContextMenuContent',
    'ContextMenuItem', 'ContextMenuSeparator', 'ContextMenuCheckboxItem',
  ],
  loader: () =>
    import('./shadcn/overlay').then((m) => ({
      Dialog: m.Dialog, DialogTrigger: m.DialogTrigger, DialogContent: m.DialogContent,
      DialogHeader: m.DialogHeader, DialogFooter: m.DialogFooter,
      DialogTitle: m.DialogTitle, DialogDescription: m.DialogDescription,
      DialogAction: m.DialogAction, DialogCancel: m.DialogCancel,
      Drawer: m.Drawer, DrawerTrigger: m.DrawerTrigger, DrawerContent: m.DrawerContent,
      DrawerHeader: m.DrawerHeader, DrawerFooter: m.DrawerFooter,
      DrawerTitle: m.DrawerTitle, DrawerDescription: m.DrawerDescription,
      DrawerClose: m.DrawerClose,
      Sheet: m.Sheet, SheetTrigger: m.SheetTrigger, SheetContent: m.SheetContent,
      SheetHeader: m.SheetHeader, SheetFooter: m.SheetFooter,
      SheetTitle: m.SheetTitle, SheetDescription: m.SheetDescription,
      SheetClose: m.SheetClose,
      HoverCard: m.HoverCard, HoverCardTrigger: m.HoverCardTrigger,
      HoverCardContent: m.HoverCardContent,
      Popover: m.Popover, PopoverTrigger: m.PopoverTrigger, PopoverContent: m.PopoverContent,
      DropdownMenu: m.DropdownMenu, DropdownMenuTrigger: m.DropdownMenuTrigger,
      DropdownMenuContent: m.DropdownMenuContent, DropdownMenuItem: m.DropdownMenuItem,
      DropdownMenuLabel: m.DropdownMenuLabel, DropdownMenuSeparator: m.DropdownMenuSeparator,
      DropdownMenuCheckboxItem: m.DropdownMenuCheckboxItem,
      DropdownMenuRadioGroup: m.DropdownMenuRadioGroup, DropdownMenuRadioItem: m.DropdownMenuRadioItem,
      DropdownMenuSub: m.DropdownMenuSub, DropdownMenuSubTrigger: m.DropdownMenuSubTrigger,
      DropdownMenuSubContent: m.DropdownMenuSubContent,
      ContextMenu: m.ContextMenu, ContextMenuTrigger: m.ContextMenuTrigger,
      ContextMenuContent: m.ContextMenuContent, ContextMenuItem: m.ContextMenuItem,
      ContextMenuSeparator: m.ContextMenuSeparator,
      ContextMenuCheckboxItem: m.ContextMenuCheckboxItem,
    })),
});

componentRegistry.registerLazyChunk({
  name: 'charts',
  componentNames: [
    'ChartContainer', 'ChartTooltip', 'ChartTooltipContent',
    'ChartLegend', 'ChartLegendContent',
    'AreaChart', 'Area', 'BarChart', 'Bar', 'LineChart', 'Line',
    'PieChart', 'Pie', 'PieLabel', 'Sector',
    'RadarChart', 'Radar', 'PolarGrid', 'PolarAngleAxis', 'PolarRadiusAxis',
    'RadialBarChart', 'RadialBar',
    'ScatterChart', 'Scatter', 'ZAxis',
    'ComposedChart', 'FunnelChart', 'Funnel', 'Treemap', 'Sankey',
    'XAxis', 'YAxis', 'CartesianGrid',
    'ReferenceLine', 'ReferenceArea', 'ReferenceDot',
    'Brush', 'Cell', 'LabelList', 'ChartLabel', 'ErrorBar',
  ],
  loader: async () => {
    const [chart, area, bar, line, pie, radar, radial, scatter, composed, funnel, treemap, sankey, utils] = await Promise.all([
      import('./charts/chart'),
      import('./charts/area-chart'),
      import('./charts/bar-chart'),
      import('./charts/line-chart'),
      import('./charts/pie-chart'),
      import('./charts/radar-chart'),
      import('./charts/radial-chart'),
      import('./charts/scatter-chart'),
      import('./charts/composed-chart'),
      import('./charts/funnel-chart'),
      import('./charts/treemap'),
      import('./charts/sankey'),
      import('./charts/utils'),
    ]);
    return {
      ChartContainer: chart.ChartContainer, ChartTooltip: chart.ChartTooltip,
      ChartTooltipContent: chart.ChartTooltipContent,
      ChartLegend: chart.ChartLegend, ChartLegendContent: chart.ChartLegendContent,
      AreaChart: area.AreaChart, Area: area.Area,
      BarChart: bar.BarChart, Bar: bar.Bar,
      LineChart: line.LineChart, Line: line.Line,
      PieChart: pie.PieChart, Pie: pie.Pie, PieLabel: pie.PieLabel, Sector: pie.Sector,
      RadarChart: radar.RadarChart, Radar: radar.Radar,
      PolarGrid: radar.PolarGrid, PolarAngleAxis: radar.PolarAngleAxis,
      PolarRadiusAxis: radar.PolarRadiusAxis,
      RadialBarChart: radial.RadialBarChart, RadialBar: radial.RadialBar,
      ScatterChart: scatter.ScatterChart, Scatter: scatter.Scatter, ZAxis: scatter.ZAxis,
      ComposedChart: composed.ComposedChart,
      FunnelChart: funnel.FunnelChart, Funnel: funnel.Funnel,
      Treemap: treemap.Treemap,
      Sankey: sankey.Sankey,
      XAxis: utils.XAxis, YAxis: utils.YAxis, CartesianGrid: utils.CartesianGrid,
      ReferenceLine: utils.ReferenceLine, ReferenceArea: utils.ReferenceArea,
      ReferenceDot: utils.ReferenceDot,
      Brush: utils.Brush, Cell: utils.Cell, LabelList: utils.LabelList,
      ChartLabel: utils.Label, ErrorBar: utils.ErrorBar,
    };
  },
});

