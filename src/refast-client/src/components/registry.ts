import React from 'react';

// Import base components
import { Container, Text, Fragment } from './base';

// Import shadcn components
import { Row, Column, Grid, Flex, Center } from './shadcn/layout';
import { Button, IconButton } from './shadcn/button';
import { Icon } from './shadcn/icon';
import { Card, CardHeader, CardContent, CardFooter, CardTitle, CardDescription } from './shadcn/card';
import { Input, Textarea, Select, SelectOption, Checkbox, Radio, RadioGroup, CheckboxGroup } from './shadcn/input';
import { Slot } from './shadcn/slot';
import { Heading, Paragraph, Link, Code, BlockQuote, List, ListItem, Label, Markdown } from './shadcn/typography';
import { Alert, AlertTitle, AlertDescription, Badge, Progress, Spinner, Skeleton } from './shadcn/feedback';
import { ConnectionStatus } from './shadcn/ConnectionStatus';
import { Table, TableHeader, TableBody, TableRow, TableHead, TableCell, Avatar, Image, Tooltip, Tabs, TabItem, Accordion, AccordionItem, AccordionTrigger, AccordionContent } from './shadcn/data_display';

// Import new Stage 9 components - Controls
import { Switch, Slider, Toggle, ToggleGroup, ToggleGroupItem, DatePicker, Calendar, Combobox, InputOTP, InputOTPGroup, InputOTPSlot, InputOTPSeparator } from './shadcn/controls';

// Import new Stage 9 components - Navigation
import {
  Breadcrumb, BreadcrumbList, BreadcrumbItem, BreadcrumbLink, BreadcrumbPage, BreadcrumbSeparator, BreadcrumbEllipsis,
  NavigationMenu, NavigationMenuList, NavigationMenuItem, NavigationMenuTrigger, NavigationMenuContent, NavigationMenuLink,
  Pagination, PaginationContent, PaginationItem, PaginationLink, PaginationPrevious, PaginationNext, PaginationEllipsis,
  Menubar, MenubarMenu, MenubarTrigger, MenubarContent, MenubarItem, MenubarSeparator, MenubarCheckboxItem, MenubarRadioGroup, MenubarRadioItem, MenubarSub, MenubarSubTrigger, MenubarSubContent,
  Command, CommandInput, CommandList, CommandEmpty, CommandGroup, CommandItem, CommandSeparator, CommandShortcut,
  SidebarProvider, Sidebar, SidebarInset, SidebarHeader, SidebarContent, SidebarFooter, SidebarSeparator,
  SidebarGroup, SidebarGroupLabel, SidebarGroupAction, SidebarGroupContent,
  SidebarMenu, SidebarMenuItem, SidebarMenuButton, SidebarMenuAction, SidebarMenuBadge,
  SidebarMenuSub, SidebarMenuSubItem, SidebarMenuSubButton, SidebarMenuSkeleton,
  SidebarRail, SidebarTrigger
} from './shadcn/navigation';

// Import new Stage 9 components - Overlay
import {
  Dialog, DialogTrigger, DialogContent, DialogHeader, DialogFooter,
  DialogTitle, DialogDescription, DialogAction, DialogCancel,
  Drawer, DrawerClose, DrawerContent, DrawerDescription, DrawerFooter, DrawerHeader, DrawerTitle, DrawerTrigger,
  Sheet, SheetTrigger, SheetContent, SheetHeader, SheetFooter,
  SheetTitle, SheetDescription, SheetClose,
  HoverCard, HoverCardTrigger, HoverCardContent,
  Popover, PopoverTrigger, PopoverContent,
  DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem,
  DropdownMenuLabel, DropdownMenuSeparator, DropdownMenuCheckboxItem,
  DropdownMenuRadioGroup, DropdownMenuRadioItem, DropdownMenuSub,
  DropdownMenuSubTrigger, DropdownMenuSubContent,
  ContextMenu, ContextMenuTrigger, ContextMenuContent, ContextMenuItem,
  ContextMenuSeparator, ContextMenuCheckboxItem
} from './shadcn/overlay';

// Import new Stage 9 components - Utility
import {
  Separator, AspectRatio, ScrollArea, Collapsible, CollapsibleTrigger, CollapsibleContent,
  Carousel, CarouselContent, CarouselItem, CarouselPrevious, CarouselNext,
  ResizablePanelGroup, ResizablePanel, ResizableHandle, ThemeSwitcher
} from './shadcn/utility';

// Import chart components
import {
  ChartContainer, ChartTooltip, ChartTooltipContent,
  ChartLegend, ChartLegendContent
} from './charts/chart';
import { AreaChart, Area } from './charts/area-chart';
import { BarChart, Bar } from './charts/bar-chart';
import { LineChart, Line } from './charts/line-chart';
import { PieChart, Pie, PieLabel, Sector } from './charts/pie-chart';
import { RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis } from './charts/radar-chart';
import { RadialBarChart, RadialBar } from './charts/radial-chart';
import { ScatterChart, Scatter, ZAxis } from './charts/scatter-chart';
import { ComposedChart } from './charts/composed-chart';
import { FunnelChart, Funnel } from './charts/funnel-chart';
import { Treemap } from './charts/treemap';
import { Sankey } from './charts/sankey';
import { XAxis, YAxis, CartesianGrid, ReferenceLine, ReferenceArea, ReferenceDot, Brush, Cell, LabelList, Label as ChartLabel, ErrorBar } from './charts/utils';

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
componentRegistry.register('Grid', Grid);
componentRegistry.register('Flex', Flex);
componentRegistry.register('Center', Center);

// Register button components
componentRegistry.register('Button', Button);
componentRegistry.register('IconButton', IconButton);
componentRegistry.register('Icon', Icon);

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
componentRegistry.register('CheckboxGroup', CheckboxGroup);
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
componentRegistry.register('Markdown', Markdown);

// Register feedback components
componentRegistry.register('Alert', Alert);
componentRegistry.register('AlertTitle', AlertTitle);
componentRegistry.register('AlertDescription', AlertDescription);
componentRegistry.register('Badge', Badge);
componentRegistry.register('Progress', Progress);
componentRegistry.register('Spinner', Spinner);
componentRegistry.register('Skeleton', Skeleton);
componentRegistry.register('ConnectionStatus', ConnectionStatus);

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
componentRegistry.register('Tabs', Tabs);
componentRegistry.register('TabItem', TabItem);
componentRegistry.register('Accordion', Accordion);
componentRegistry.register('AccordionItem', AccordionItem);
componentRegistry.register('AccordionTrigger', AccordionTrigger);
componentRegistry.register('AccordionContent', AccordionContent);

// Register control components (Stage 9)
componentRegistry.register('Switch', Switch);
componentRegistry.register('Slider', Slider);
componentRegistry.register('Toggle', Toggle);
componentRegistry.register('ToggleGroup', ToggleGroup);
componentRegistry.register('ToggleGroupItem', ToggleGroupItem);
componentRegistry.register('DatePicker', DatePicker);
componentRegistry.register('Calendar', Calendar);
componentRegistry.register('Combobox', Combobox);
componentRegistry.register('InputOTP', InputOTP);
componentRegistry.register('InputOTPGroup', InputOTPGroup);
componentRegistry.register('InputOTPSlot', InputOTPSlot);
componentRegistry.register('InputOTPSeparator', InputOTPSeparator);

// Register navigation components (Stage 9)
componentRegistry.register('Breadcrumb', Breadcrumb);
componentRegistry.register('BreadcrumbList', BreadcrumbList);
componentRegistry.register('BreadcrumbItem', BreadcrumbItem);
componentRegistry.register('BreadcrumbLink', BreadcrumbLink);
componentRegistry.register('BreadcrumbPage', BreadcrumbPage);
componentRegistry.register('BreadcrumbSeparator', BreadcrumbSeparator);
componentRegistry.register('BreadcrumbEllipsis', BreadcrumbEllipsis);
componentRegistry.register('NavigationMenu', NavigationMenu);
componentRegistry.register('NavigationMenuList', NavigationMenuList);
componentRegistry.register('NavigationMenuItem', NavigationMenuItem);
componentRegistry.register('NavigationMenuTrigger', NavigationMenuTrigger);
componentRegistry.register('NavigationMenuContent', NavigationMenuContent);
componentRegistry.register('NavigationMenuLink', NavigationMenuLink);
componentRegistry.register('Pagination', Pagination);
componentRegistry.register('PaginationContent', PaginationContent);
componentRegistry.register('PaginationItem', PaginationItem);
componentRegistry.register('PaginationLink', PaginationLink);
componentRegistry.register('PaginationPrevious', PaginationPrevious);
componentRegistry.register('PaginationNext', PaginationNext);
componentRegistry.register('PaginationEllipsis', PaginationEllipsis);
componentRegistry.register('Menubar', Menubar);
componentRegistry.register('MenubarMenu', MenubarMenu);
componentRegistry.register('MenubarTrigger', MenubarTrigger);
componentRegistry.register('MenubarContent', MenubarContent);
componentRegistry.register('MenubarItem', MenubarItem);
componentRegistry.register('MenubarSeparator', MenubarSeparator);
componentRegistry.register('MenubarCheckboxItem', MenubarCheckboxItem);
componentRegistry.register('MenubarRadioGroup', MenubarRadioGroup);
componentRegistry.register('MenubarRadioItem', MenubarRadioItem);
componentRegistry.register('MenubarSub', MenubarSub);
componentRegistry.register('MenubarSubTrigger', MenubarSubTrigger);
componentRegistry.register('MenubarSubContent', MenubarSubContent);
componentRegistry.register('Command', Command);
componentRegistry.register('CommandInput', CommandInput);
componentRegistry.register('CommandList', CommandList);
componentRegistry.register('CommandEmpty', CommandEmpty);
componentRegistry.register('CommandGroup', CommandGroup);
componentRegistry.register('CommandItem', CommandItem);
componentRegistry.register('CommandSeparator', CommandSeparator);
componentRegistry.register('CommandShortcut', CommandShortcut);
componentRegistry.register('SidebarProvider', SidebarProvider);
componentRegistry.register('Sidebar', Sidebar);
componentRegistry.register('SidebarInset', SidebarInset);
componentRegistry.register('SidebarHeader', SidebarHeader);
componentRegistry.register('SidebarContent', SidebarContent);
componentRegistry.register('SidebarFooter', SidebarFooter);
componentRegistry.register('SidebarSeparator', SidebarSeparator);
componentRegistry.register('SidebarGroup', SidebarGroup);
componentRegistry.register('SidebarGroupLabel', SidebarGroupLabel);
componentRegistry.register('SidebarGroupAction', SidebarGroupAction);
componentRegistry.register('SidebarGroupContent', SidebarGroupContent);
componentRegistry.register('SidebarMenu', SidebarMenu);
componentRegistry.register('SidebarMenuItem', SidebarMenuItem);
componentRegistry.register('SidebarMenuButton', SidebarMenuButton);
componentRegistry.register('SidebarMenuAction', SidebarMenuAction);
componentRegistry.register('SidebarMenuBadge', SidebarMenuBadge);
componentRegistry.register('SidebarMenuSub', SidebarMenuSub);
componentRegistry.register('SidebarMenuSubItem', SidebarMenuSubItem);
componentRegistry.register('SidebarMenuSubButton', SidebarMenuSubButton);
componentRegistry.register('SidebarMenuSkeleton', SidebarMenuSkeleton);
componentRegistry.register('SidebarRail', SidebarRail);
componentRegistry.register('SidebarTrigger', SidebarTrigger);

// Register overlay components (Stage 9)
componentRegistry.register('Dialog', Dialog);
componentRegistry.register('DialogTrigger', DialogTrigger);
componentRegistry.register('DialogContent', DialogContent);
componentRegistry.register('DialogHeader', DialogHeader);
componentRegistry.register('DialogFooter', DialogFooter);
componentRegistry.register('DialogTitle', DialogTitle);
componentRegistry.register('DialogDescription', DialogDescription);
componentRegistry.register('DialogAction', DialogAction);
componentRegistry.register('DialogCancel', DialogCancel);
componentRegistry.register('Sheet', Sheet);
componentRegistry.register('SheetTrigger', SheetTrigger);
componentRegistry.register('SheetContent', SheetContent);
componentRegistry.register('SheetHeader', SheetHeader);
componentRegistry.register('SheetFooter', SheetFooter);
componentRegistry.register('SheetTitle', SheetTitle);
componentRegistry.register('SheetDescription', SheetDescription);
componentRegistry.register('SheetClose', SheetClose);
componentRegistry.register('Drawer', Drawer);
componentRegistry.register('DrawerTrigger', DrawerTrigger);
componentRegistry.register('DrawerContent', DrawerContent);
componentRegistry.register('DrawerHeader', DrawerHeader);
componentRegistry.register('DrawerFooter', DrawerFooter);
componentRegistry.register('DrawerTitle', DrawerTitle);
componentRegistry.register('DrawerDescription', DrawerDescription);
componentRegistry.register('DrawerClose', DrawerClose);
componentRegistry.register('HoverCard', HoverCard);
componentRegistry.register('HoverCardTrigger', HoverCardTrigger);
componentRegistry.register('HoverCardContent', HoverCardContent);
componentRegistry.register('Popover', Popover);
componentRegistry.register('PopoverTrigger', PopoverTrigger);
componentRegistry.register('PopoverContent', PopoverContent);
componentRegistry.register('DropdownMenu', DropdownMenu);
componentRegistry.register('DropdownMenuTrigger', DropdownMenuTrigger);
componentRegistry.register('DropdownMenuContent', DropdownMenuContent);
componentRegistry.register('DropdownMenuItem', DropdownMenuItem);
componentRegistry.register('DropdownMenuLabel', DropdownMenuLabel);
componentRegistry.register('DropdownMenuSeparator', DropdownMenuSeparator);
componentRegistry.register('DropdownMenuCheckboxItem', DropdownMenuCheckboxItem);
componentRegistry.register('DropdownMenuRadioGroup', DropdownMenuRadioGroup);
componentRegistry.register('DropdownMenuRadioItem', DropdownMenuRadioItem);
componentRegistry.register('DropdownMenuSub', DropdownMenuSub);
componentRegistry.register('DropdownMenuSubTrigger', DropdownMenuSubTrigger);
componentRegistry.register('DropdownMenuSubContent', DropdownMenuSubContent);
componentRegistry.register('ContextMenu', ContextMenu);
componentRegistry.register('ContextMenuTrigger', ContextMenuTrigger);
componentRegistry.register('ContextMenuContent', ContextMenuContent);
componentRegistry.register('ContextMenuItem', ContextMenuItem);
componentRegistry.register('ContextMenuSeparator', ContextMenuSeparator);
componentRegistry.register('ContextMenuCheckboxItem', ContextMenuCheckboxItem);

// Register utility components (Stage 9)
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

// Register chart components (Stage 10)
componentRegistry.register('ChartContainer', ChartContainer);
componentRegistry.register('ChartTooltip', ChartTooltip);
componentRegistry.register('ChartTooltipContent', ChartTooltipContent);
componentRegistry.register('ChartLegend', ChartLegend);
componentRegistry.register('ChartLegendContent', ChartLegendContent);
componentRegistry.register('AreaChart', AreaChart);
componentRegistry.register('Area', Area);
componentRegistry.register('XAxis', XAxis);
componentRegistry.register('YAxis', YAxis);
componentRegistry.register('CartesianGrid', CartesianGrid);
componentRegistry.register('ReferenceLine', ReferenceLine);
componentRegistry.register('ReferenceArea', ReferenceArea);
componentRegistry.register('ReferenceDot', ReferenceDot);
componentRegistry.register('Brush', Brush);
componentRegistry.register('Cell', Cell);
componentRegistry.register('LabelList', LabelList);
componentRegistry.register('ChartLabel', ChartLabel);
componentRegistry.register('ErrorBar', ErrorBar);
componentRegistry.register('BarChart', BarChart);
componentRegistry.register('Bar', Bar);
componentRegistry.register('LineChart', LineChart);
componentRegistry.register('Line', Line);
componentRegistry.register('PieChart', PieChart);
componentRegistry.register('Pie', Pie);
componentRegistry.register('PieLabel', PieLabel);
componentRegistry.register('Sector', Sector);
componentRegistry.register('RadarChart', RadarChart);
componentRegistry.register('Radar', Radar);
componentRegistry.register('PolarGrid', PolarGrid);
componentRegistry.register('PolarAngleAxis', PolarAngleAxis);
componentRegistry.register('PolarRadiusAxis', PolarRadiusAxis);
componentRegistry.register('RadialBarChart', RadialBarChart);
componentRegistry.register('RadialBar', RadialBar);
componentRegistry.register('ScatterChart', ScatterChart);
componentRegistry.register('Scatter', Scatter);
componentRegistry.register('ZAxis', ZAxis);
componentRegistry.register('ComposedChart', ComposedChart);
componentRegistry.register('FunnelChart', FunnelChart);
componentRegistry.register('Funnel', Funnel);
componentRegistry.register('Treemap', Treemap);
componentRegistry.register('Sankey', Sankey);

