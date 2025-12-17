"""Refast component system."""

from refast.components.base import Component, Container, Fragment, Text
from refast.components.registry import (
    ReactComponent,
    clear_registry,
    get_component,
    list_components,
    register_component,
)

# Re-export shadcn components
from refast.components.shadcn import (
    Accordion,
    # Feedback
    Alert,
    Avatar,
    Badge,
    # Button
    Button,
    # Card
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
    Center,
    Checkbox,
    Code,
    Column,
    DataTable,
    Dialog,
    Divider,
    Flex,
    # Form
    Form,
    FormField,
    Grid,
    # Typography
    Heading,
    IconButton,
    # Input
    Input,
    Label,
    Link,
    List,
    Modal,
    Paragraph,
    Progress,
    Radio,
    # Layout
    Row,
    Select,
    Skeleton,
    Spacer,
    Spinner,
    Stack,
    TabItem,
    # Data Display
    Table,
    Tabs,
    Textarea,
    Toast,
    Tooltip,
)
from refast.components.slot import Slot

__all__ = [
    # Base
    "Component",
    "Container",
    "Text",
    "Fragment",
    "Slot",
    # Registry
    "register_component",
    "get_component",
    "list_components",
    "ReactComponent",
    "clear_registry",
    # Layout
    "Row",
    "Column",
    "Stack",
    "Grid",
    "Flex",
    "Center",
    "Spacer",
    "Divider",
    # Button
    "Button",
    "IconButton",
    # Card
    "Card",
    "CardHeader",
    "CardContent",
    "CardFooter",
    "CardTitle",
    "CardDescription",
    # Input
    "Input",
    "Textarea",
    "Select",
    "Checkbox",
    "Radio",
    # Form
    "Form",
    "FormField",
    "Label",
    # Feedback
    "Alert",
    "Toast",
    "Modal",
    "Dialog",
    "Spinner",
    "Progress",
    "Skeleton",
    # Data Display
    "Table",
    "DataTable",
    "List",
    "Badge",
    "Avatar",
    "Tooltip",
    "Tabs",
    "TabItem",
    "Accordion",
    # Typography
    "Heading",
    "Paragraph",
    "Code",
    "Link",
]
