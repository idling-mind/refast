"""Tests for explicit style kwargs on visual components."""

from refast.components.base import Container
from refast.components.shadcn.button import Button
from refast.components.shadcn.data_display import DataTable, Table
from refast.components.shadcn.feedback import Alert
from refast.components.shadcn.input import Input
from refast.components.shadcn.layout import Row
from refast.components.shadcn.navigation import NavigationMenu


def test_container_accepts_explicit_parent_style() -> None:
    component = Container(style={"margin": "8px"}, parent_style={"display": "grid"})
    rendered = component.render()

    assert rendered["props"]["style"] == {"margin": "8px"}
    assert rendered["props"]["parent_style"] == {"display": "grid"}


def test_button_accepts_explicit_style() -> None:
    button = Button("Save", style={"color": "red"})
    rendered = button.render()

    assert rendered["props"]["style"] == {"color": "red"}


def test_input_accepts_explicit_style() -> None:
    input_component = Input(name="email", style={"width": "100%"})
    rendered = input_component.render()

    assert rendered["props"]["style"] == {"width": "100%"}


def test_row_accepts_explicit_style_and_parent_style() -> None:
    row = Row(style={"gap": "1rem"}, parent_style={"padding": "12px"})
    rendered = row.render()

    assert rendered["props"]["style"] == {"gap": "1rem"}
    assert rendered["props"]["parent_style"] == {"padding": "12px"}


def test_alert_accepts_explicit_style() -> None:
    alert = Alert(message="Heads up", style={"borderWidth": "2px"})
    rendered = alert.render()

    assert rendered["props"]["style"] == {"borderWidth": "2px"}


def test_navigation_menu_accepts_explicit_style_and_parent_style() -> None:
    menu = NavigationMenu(style={"minHeight": "24px"}, parent_style={"width": "100%"})
    rendered = menu.render()

    assert rendered["props"]["style"] == {"minHeight": "24px"}
    assert rendered["props"]["parent_style"] == {"width": "100%"}


def test_table_accepts_explicit_style_and_parent_style() -> None:
    table = Table(style={"borderCollapse": "collapse"}, parent_style={"overflowX": "auto"})
    rendered = table.render()

    assert rendered["props"]["style"] == {"borderCollapse": "collapse"}
    assert rendered["props"]["parent_style"] == {"overflowX": "auto"}


def test_data_table_accepts_explicit_style_and_parent_style() -> None:
    table = DataTable(columns=[], data=[], style={"fontSize": "12px"}, parent_style={"padding": "4px"})
    rendered = table.render()

    assert rendered["props"]["style"] == {"fontSize": "12px"}
    assert rendered["props"]["parent_style"] == {"padding": "4px"}
