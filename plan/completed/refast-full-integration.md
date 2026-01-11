# Recharts Full Coverage Plan for Refast

## Current State Analysis

### Currently Implemented Chart Types
| Chart Type | Python | React |
|------------|--------|-------|
| AreaChart | ✅ | ✅ |
| BarChart | ✅ | ✅ |
| LineChart | ✅ | ✅ |
| PieChart | ✅ | ✅ |
| RadarChart | ✅ | ✅ |
| RadialBarChart | ✅ | ✅ |

### Missing Chart Types
| Chart Type | Description |
|------------|-------------|
| **ScatterChart** | 2D/3D scatter plots with X, Y, Z axes |
| **ComposedChart** | Mixed chart combining Bar, Line, Area |
| **FunnelChart** | Funnel/pyramid visualization |
| **Treemap** | Hierarchical data visualization |
| **Sankey** | Flow diagram showing relationships |
| **SunburstChart** | Hierarchical sunburst diagram |

---

## Missing Props by Component

### 1. ChartContainer (ResponsiveContainer wrapper)
**Current Props:** `config`, `width`, `height`, `min_height`, `min_width`, `max_height`, `aspect`, `debounce`, `initial_dimension`, `on_resize`

**Missing Props:** None - fully covered ✅

---

### 2. AreaChart
**Current Props:** `data`, `margin`, `stack_offset`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `layout` | `"horizontal" \| "vertical"` | Chart layout direction |
| `sync_id` | `str` | ID for syncing multiple charts |
| `sync_method` | `"index" \| "value"` | How to sync charts |
| `base_value` | `int \| "dataMin" \| "dataMax" \| "auto"` | Base value for area |
| `on_click` | `Callback` | Click event handler |
| `on_mouse_enter` | `Callback` | Mouse enter handler |
| `on_mouse_leave` | `Callback` | Mouse leave handler |
| `on_mouse_move` | `Callback` | Mouse move handler |

---

### 3. Area
**Current Props:** `data_key`, `type`, `fill`, `fill_opacity`, `stroke`, `stroke_width`, `stacked_id`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `base_value` | `int \| "dataMin" \| "dataMax"` | Baseline value |
| `base_line` | `int \| list[dict]` | Custom baseline |
| `connect_nulls` | `bool` | Connect across null points |
| `dot` | `bool \| dict` | Dot configuration |
| `active_dot` | `bool \| dict` | Active dot config |
| `label` | `bool \| dict` | Label configuration |
| `legend_type` | `str` | Legend icon type |
| `name` | `str` | Name for tooltip/legend |
| `unit` | `str` | Unit for tooltip |
| `x_axis_id` | `str \| int` | XAxis reference |
| `y_axis_id` | `str \| int` | YAxis reference |
| `is_animation_active` | `bool \| "auto"` | Enable animation |
| `animation_begin` | `int` | Animation delay (ms) |
| `animation_duration` | `int` | Animation duration (ms) |
| `animation_easing` | `str` | Easing function |
| `hide` | `bool` | Hide the area |

---

### 4. BarChart
**Current Props:** `data`, `margin`, `bar_category_gap`, `bar_gap`, `bar_size`, `layout`, `stack_offset`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `sync_id` | `str` | ID for syncing multiple charts |
| `sync_method` | `"index" \| "value"` | How to sync charts |
| `reverse_stack_order` | `bool` | Reverse stacking order |
| `on_click` | `Callback` | Click event handler |
| `on_mouse_enter` | `Callback` | Mouse enter handler |
| `on_mouse_leave` | `Callback` | Mouse leave handler |
| `on_mouse_move` | `Callback` | Mouse move handler |
| `max_bar_size` | `int` | Maximum bar width |

---

### 5. Bar
**Current Props:** `data_key`, `fill`, `radius`, `bar_size`, `bar_gap`, `stack_id`, `background`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `x_axis_id` | `str \| int` | XAxis reference |
| `y_axis_id` | `str \| int` | YAxis reference |
| `min_point_size` | `int` | Minimum bar height for 0 values |
| `max_bar_size` | `int` | Maximum bar size |
| `name` | `str` | Name for tooltip/legend |
| `unit` | `str` | Unit for tooltip |
| `legend_type` | `str` | Legend icon type |
| `label` | `bool \| dict` | Label configuration |
| `shape` | `str \| Component` | Custom shape |
| `active_bar` | `bool \| dict` | Active bar styling |
| `is_animation_active` | `bool \| "auto"` | Enable animation |
| `animation_begin` | `int` | Animation delay (ms) |
| `animation_duration` | `int` | Animation duration (ms) |
| `animation_easing` | `str` | Easing function |
| `hide` | `bool` | Hide the bar |

---

### 6. LineChart
**Current Props:** `data`, `margin`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `layout` | `"horizontal" \| "vertical"` | Chart layout |
| `sync_id` | `str` | ID for syncing multiple charts |
| `sync_method` | `"index" \| "value"` | How to sync charts |
| `on_click` | `Callback` | Click event handler |
| `on_mouse_enter` | `Callback` | Mouse enter handler |
| `on_mouse_leave` | `Callback` | Mouse leave handler |
| `on_mouse_move` | `Callback` | Mouse move handler |

---

### 7. Line
**Current Props:** `data_key`, `type`, `stroke`, `stroke_width`, `dot`, `active_dot`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `connect_nulls` | `bool` | Connect across null points |
| `x_axis_id` | `str \| int` | XAxis reference |
| `y_axis_id` | `str \| int` | YAxis reference |
| `legend_type` | `str` | Legend icon type |
| `name` | `str` | Name for tooltip/legend |
| `unit` | `str` | Unit for tooltip |
| `label` | `bool \| dict` | Label configuration |
| `stroke_dasharray` | `str` | Dash pattern |
| `is_animation_active` | `bool \| "auto"` | Enable animation |
| `animation_begin` | `int` | Animation delay (ms) |
| `animation_duration` | `int` | Animation duration (ms) |
| `animation_easing` | `str` | Easing function |
| `hide` | `bool` | Hide the line |

---

### 8. PieChart
**Current Props:** `margin`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `on_click` | `Callback` | Click event handler |
| `on_mouse_enter` | `Callback` | Mouse enter handler |
| `on_mouse_leave` | `Callback` | Mouse leave handler |

---

### 9. Pie
**Current Props:** `data`, `data_key`, `name_key`, `cx`, `cy`, `inner_radius`, `outer_radius`, `label`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `start_angle` | `int` | Start angle (degrees) |
| `end_angle` | `int` | End angle (degrees) |
| `padding_angle` | `int` | Padding between sectors |
| `corner_radius` | `int \| str` | Corner radius |
| `min_angle` | `int` | Minimum sector angle |
| `label_line` | `bool \| dict` | Label line config |
| `legend_type` | `str` | Legend icon type |
| `active_shape` | `dict \| Component` | Active sector styling |
| `inactive_shape` | `dict \| Component` | Inactive sector styling |
| `is_animation_active` | `bool \| "auto"` | Enable animation |
| `animation_begin` | `int` | Animation delay (ms) |
| `animation_duration` | `int` | Animation duration (ms) |
| `animation_easing` | `str` | Easing function |
| `hide` | `bool` | Hide the pie |

---

### 10. RadarChart
**Current Props:** `data`, `margin`, `cx`, `cy`, `inner_radius`, `outer_radius`, `start_angle`, `end_angle`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `on_click` | `Callback` | Click event handler |
| `on_mouse_enter` | `Callback` | Mouse enter handler |
| `on_mouse_leave` | `Callback` | Mouse leave handler |

---

### 11. Radar
**Current Props:** `data_key`, `fill`, `fill_opacity`, `stroke`, `stroke_width`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `dot` | `bool \| dict` | Dot configuration |
| `active_dot` | `bool \| dict` | Active dot config |
| `label` | `bool \| dict` | Label configuration |
| `legend_type` | `str` | Legend icon type |
| `name` | `str` | Name for tooltip/legend |
| `angle_axis_id` | `str \| int` | Angle axis reference |
| `radius_axis_id` | `str \| int` | Radius axis reference |
| `is_animation_active` | `bool \| "auto"` | Enable animation |
| `animation_begin` | `int` | Animation delay (ms) |
| `animation_duration` | `int` | Animation duration (ms) |
| `animation_easing` | `str` | Easing function |
| `hide` | `bool` | Hide the radar |

---

### 12. RadialBarChart
**Current Props:** `data`, `margin`, `cx`, `cy`, `inner_radius`, `outer_radius`, `bar_size`, `start_angle`, `end_angle`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `bar_category_gap` | `str \| int` | Gap between categories |
| `bar_gap` | `str \| int` | Gap between bars |
| `on_click` | `Callback` | Click event handler |
| `on_mouse_enter` | `Callback` | Mouse enter handler |
| `on_mouse_leave` | `Callback` | Mouse leave handler |

---

### 13. RadialBar
**Current Props:** `data_key`, `min_angle`, `background`, `label`, `corner_radius`, `fill`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `angle_axis_id` | `str \| int` | Angle axis reference |
| `radius_axis_id` | `str \| int` | Radius axis reference |
| `legend_type` | `str` | Legend icon type |
| `max_bar_size` | `int` | Maximum bar size |
| `stack_id` | `str` | Stack identifier |
| `force_corner_radius` | `bool` | Force corner radius |
| `corner_is_external` | `bool` | Corner on external edge |
| `shape` | `Component` | Custom shape |
| `active_shape` | `dict \| Component` | Active bar styling |
| `is_animation_active` | `bool \| "auto"` | Enable animation |
| `animation_begin` | `int` | Animation delay (ms) |
| `animation_duration` | `int` | Animation duration (ms) |
| `animation_easing` | `str` | Easing function |
| `hide` | `bool` | Hide the bar |

---

### 14. XAxis
**Current Props:** `data_key`, `orientation`, `type`, `hide`, `tick_line`, `axis_line`, `tick_margin`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `x_axis_id` | `str \| int` | Unique axis ID |
| `height` | `int` | Axis height |
| `width` | `int` | Axis width |
| `allow_decimals` | `bool` | Allow decimal ticks |
| `allow_data_overflow` | `bool` | Allow overflow |
| `allow_duplicated_category` | `bool` | Allow duplicate categories |
| `scale` | `str` | Scale type |
| `domain` | `list` | Axis domain |
| `ticks` | `list` | Custom tick values |
| `tick_count` | `int` | Number of ticks |
| `tick_size` | `int` | Tick size |
| `tick_formatter` | `Callback` | Tick formatter |
| `tick` | `bool \| dict \| Component` | Tick config |
| `interval` | `int \| str` | Tick interval |
| `padding` | `dict` | Left/right padding |
| `mirror` | `bool` | Mirror axis |
| `reversed` | `bool` | Reverse axis |
| `label` | `str \| dict \| Component` | Axis label |
| `angle` | `int` | Tick rotation angle |
| `min_tick_gap` | `int` | Minimum gap between ticks |
| `unit` | `str` | Unit for axis |
| `name` | `str` | Name for axis |
| `include_hidden` | `bool` | Include hidden series |

---

### 15. YAxis
**Current Props:** `data_key`, `orientation`, `type`, `hide`, `tick_line`, `axis_line`, `tick_margin`

**Missing Props:** (Same as XAxis above, plus:)
| Prop | Type | Description |
|------|------|-------------|
| `y_axis_id` | `str \| int` | Unique axis ID |
| `width` | `int \| "auto"` | Axis width |

---

### 16. CartesianGrid
**Current Props:** `stroke_dasharray`, `vertical`, `horizontal`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `x` | `int` | X position |
| `y` | `int` | Y position |
| `width` | `int` | Grid width |
| `height` | `int` | Grid height |
| `horizontal_points` | `list[int]` | Custom horizontal lines |
| `vertical_points` | `list[int]` | Custom vertical lines |
| `horizontal_values` | `list` | Values for horizontal lines |
| `vertical_values` | `list` | Values for vertical lines |
| `horizontal_fill` | `list[str]` | Stripe fill colors |
| `vertical_fill` | `list[str]` | Stripe fill colors |
| `fill` | `str` | Background fill |
| `fill_opacity` | `float` | Fill opacity |
| `stroke` | `str` | Line color |
| `sync_with_ticks` | `bool` | Sync with axis ticks |
| `x_axis_id` | `str \| int` | XAxis reference |
| `y_axis_id` | `str \| int` | YAxis reference |

---

### 17. PolarGrid
**Current Props:** (only `**kwargs`)

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `cx` | `int` | Center X |
| `cy` | `int` | Center Y |
| `inner_radius` | `int` | Inner radius |
| `outer_radius` | `int` | Outer radius |
| `polar_angles` | `list[int]` | Angle lines |
| `polar_radius` | `list[int]` | Radius lines |
| `grid_type` | `"polygon" \| "circle"` | Grid type |
| `radial_lines` | `bool` | Show radial lines |
| `angle_axis_id` | `str \| int` | Angle axis reference |
| `radius_axis_id` | `str \| int` | Radius axis reference |
| `stroke` | `str` | Line color |
| `stroke_dasharray` | `str` | Dash pattern |

---

### 18. PolarAngleAxis
**Current Props:** `data_key`, `type`, `tick`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `angle_axis_id` | `str \| int` | Unique axis ID |
| `domain` | `list` | Axis domain |
| `ticks` | `list` | Custom tick values |
| `tick_count` | `int` | Number of ticks |
| `tick_size` | `int` | Tick size |
| `tick_line` | `bool \| dict` | Tick line config |
| `tick_formatter` | `Callback` | Tick formatter |
| `axis_line` | `bool \| dict` | Axis line config |
| `axis_line_type` | `"polygon" \| "circle"` | Axis line type |
| `orientation` | `"inner" \| "outer"` | Orientation |
| `scale` | `str` | Scale type |
| `allow_duplicated_category` | `bool` | Allow duplicates |
| `allow_decimals` | `bool` | Allow decimals |
| `reversed` | `bool` | Reverse axis |
| `stroke` | `str` | Line color |

---

### 19. PolarRadiusAxis
**Current Props:** `angle`, `type`, `tick`, `domain`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `radius_axis_id` | `str \| int` | Unique axis ID |
| `cx` | `int` | Center X |
| `cy` | `int` | Center Y |
| `ticks` | `list` | Custom tick values |
| `tick_count` | `int` | Number of ticks |
| `tick_size` | `int` | Tick size |
| `tick_line` | `bool \| dict` | Tick line config |
| `tick_formatter` | `Callback` | Tick formatter |
| `axis_line` | `bool \| dict` | Axis line config |
| `orientation` | `"left" \| "right" \| "middle"` | Orientation |
| `scale` | `str` | Scale type |
| `allow_decimals` | `bool` | Allow decimals |
| `allow_data_overflow` | `bool` | Allow overflow |
| `reversed` | `bool` | Reverse axis |
| `stroke` | `str` | Line color |

---

### 20. ReferenceLine
**Current Props:** `y`, `x`, `stroke`, `stroke_dasharray`, `label`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `x_axis_id` | `str \| int` | XAxis reference |
| `y_axis_id` | `str \| int` | YAxis reference |
| `if_overflow` | `str` | Behavior when overflow |
| `segment` | `list[dict]` | Line segment points |
| `position` | `"start" \| "middle" \| "end"` | Position in band |
| `stroke_width` | `int` | Line width |
| `shape` | `Component` | Custom shape |

---

### 21. Brush
**Current Props:** `data_key`, `height`, `stroke`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `x` | `int` | X position |
| `y` | `int` | Y position |
| `width` | `int` | Width |
| `traveller_width` | `int` | Handle width |
| `traveller` | `Component` | Custom handle |
| `gap` | `int` | Data skip gap |
| `start_index` | `int` | Initial start |
| `end_index` | `int` | Initial end |
| `tick_formatter` | `Callback` | Tick formatter |
| `fill` | `str` | Fill color |
| `padding` | `dict` | Padding |
| `always_show_text` | `bool` | Always show text |
| `on_change` | `Callback` | Change handler |

---

## Missing Components (Need to Create)

### 22. NEW: ScatterChart
| Prop | Type | Description |
|------|------|-------------|
| `data` | `list[dict]` | Chart data |
| `margin` | `dict` | Chart margins |
| `layout` | `"horizontal" \| "vertical"` | Layout |
| `on_click` | `Callback` | Click handler |
| `on_mouse_enter` | `Callback` | Mouse enter handler |
| `on_mouse_leave` | `Callback` | Mouse leave handler |

---

### 23. NEW: Scatter
| Prop | Type | Description |
|------|------|-------------|
| `data` | `list[dict]` | Scatter data |
| `data_key` | `str` | Data key |
| `x_axis_id` | `str \| int` | XAxis reference |
| `y_axis_id` | `str \| int` | YAxis reference |
| `z_axis_id` | `str \| int` | ZAxis reference |
| `line` | `bool \| dict` | Connecting line |
| `line_type` | `"joint" \| "fitting"` | Line type |
| `line_joint_type` | `str` | Line curve type |
| `shape` | `str \| Component` | Point shape |
| `active_shape` | `dict \| Component` | Active shape |
| `legend_type` | `str` | Legend icon type |
| `name` | `str` | Name for tooltip |
| `fill` | `str` | Fill color |
| `label` | `bool \| dict` | Label config |
| `is_animation_active` | `bool \| "auto"` | Animation |
| `animation_begin` | `int` | Animation delay |
| `animation_duration` | `int` | Animation duration |
| `animation_easing` | `str` | Easing function |
| `hide` | `bool` | Hide scatter |

---

### 24. NEW: ZAxis
| Prop | Type | Description |
|------|------|-------------|
| `z_axis_id` | `str \| int` | Unique axis ID |
| `data_key` | `str` | Data key |
| `type` | `"number" \| "category"` | Axis type |
| `name` | `str` | Axis name |
| `unit` | `str` | Unit |
| `range` | `list[int]` | Size range |
| `scale` | `str` | Scale type |
| `domain` | `list` | Domain |

---

### 25. NEW: ComposedChart
| Prop | Type | Description |
|------|------|-------------|
| `data` | `list[dict]` | Chart data |
| `margin` | `dict` | Chart margins |
| `layout` | `"horizontal" \| "vertical"` | Layout |
| `bar_category_gap` | `str \| int` | Bar gap |
| `bar_gap` | `str \| int` | Bar gap |
| `bar_size` | `int` | Bar size |
| `sync_id` | `str` | Sync ID |
| `sync_method` | `"index" \| "value"` | Sync method |
| `on_click` | `Callback` | Click handler |
| `on_mouse_enter` | `Callback` | Mouse enter |
| `on_mouse_leave` | `Callback` | Mouse leave |

---

### 26. NEW: FunnelChart
| Prop | Type | Description |
|------|------|-------------|
| `margin` | `dict` | Chart margins |
| `on_click` | `Callback` | Click handler |
| `on_mouse_enter` | `Callback` | Mouse enter |
| `on_mouse_leave` | `Callback` | Mouse leave |

---

### 27. NEW: Funnel
| Prop | Type | Description |
|------|------|-------------|
| `data` | `list[dict]` | Funnel data |
| `data_key` | `str` | Value key |
| `name_key` | `str` | Name key |
| `shape` | `Component` | Custom shape |
| `active_shape` | `dict \| Component` | Active shape |
| `label` | `bool \| dict` | Label config |
| `legend_type` | `str` | Legend icon |
| `last_shape_type` | `"triangle" \| "rectangle"` | Last shape |
| `reversed` | `bool` | Reverse order |
| `is_animation_active` | `bool \| "auto"` | Animation |
| `animation_begin` | `int` | Animation delay |
| `animation_duration` | `int` | Animation duration |
| `animation_easing` | `str` | Easing function |
| `hide` | `bool` | Hide funnel |

---

### 28. NEW: Treemap
| Prop | Type | Description |
|------|------|-------------|
| `data` | `list[dict]` | Treemap data |
| `width` | `int \| str` | Width |
| `height` | `int \| str` | Height |
| `data_key` | `str` | Value key |
| `name_key` | `str` | Name key |
| `aspect_ratio` | `float` | Aspect ratio |
| `type` | `"flat" \| "nest"` | Treemap type |
| `content` | `Component` | Custom content |
| `fill` | `str` | Fill color |
| `stroke` | `str` | Stroke color |
| `color_panel` | `list[str]` | Colors |
| `is_animation_active` | `bool \| "auto"` | Animation |
| `animation_begin` | `int` | Animation delay |
| `animation_duration` | `int` | Animation duration |
| `animation_easing` | `str` | Easing function |
| `on_click` | `Callback` | Click handler |
| `on_mouse_enter` | `Callback` | Mouse enter |
| `on_mouse_leave` | `Callback` | Mouse leave |

---

### 29. NEW: Sankey
| Prop | Type | Description |
|------|------|-------------|
| `data` | `dict` | Sankey data (nodes, links) |
| `width` | `int \| str` | Width |
| `height` | `int \| str` | Height |
| `data_key` | `str` | Value key |
| `name_key` | `str` | Name key |
| `node_padding` | `int` | Node padding |
| `node_width` | `int` | Node width |
| `link_curvature` | `float` | Link curvature |
| `iterations` | `int` | Layout iterations |
| `node` | `dict \| Component` | Node config |
| `link` | `dict \| Component` | Link config |
| `margin` | `dict` | Margins |
| `sort` | `bool` | Sort nodes |
| `vertical_align` | `"justify" \| "top"` | Vertical align |
| `align` | `"left" \| "justify"` | Horizontal align |
| `on_click` | `Callback` | Click handler |
| `on_mouse_enter` | `Callback` | Mouse enter |
| `on_mouse_leave` | `Callback` | Mouse leave |

---

### 30. NEW: SunburstChart
| Prop | Type | Description |
|------|------|-------------|
| `data` | `dict` | Hierarchical data |
| `width` | `int \| str` | Width |
| `height` | `int \| str` | Height |
| `data_key` | `str` | Value key |
| `name_key` | `str` | Name key |
| `cx` | `int` | Center X |
| `cy` | `int` | Center Y |
| `inner_radius` | `int` | Inner radius |
| `outer_radius` | `int` | Outer radius |
| `start_angle` | `int` | Start angle |
| `end_angle` | `int` | End angle |
| `padding` | `int` | Padding |
| `ring_padding` | `int` | Ring padding |
| `fill` | `str` | Fill color |
| `stroke` | `str` | Stroke color |
| `on_click` | `Callback` | Click handler |
| `on_mouse_enter` | `Callback` | Mouse enter |
| `on_mouse_leave` | `Callback` | Mouse leave |

---

### 31. NEW: ReferenceArea
| Prop | Type | Description |
|------|------|-------------|
| `x1` | `int \| str` | Start X |
| `x2` | `int \| str` | End X |
| `y1` | `int \| str` | Start Y |
| `y2` | `int \| str` | End Y |
| `x_axis_id` | `str \| int` | XAxis reference |
| `y_axis_id` | `str \| int` | YAxis reference |
| `if_overflow` | `str` | Overflow behavior |
| `fill` | `str` | Fill color |
| `fill_opacity` | `float` | Fill opacity |
| `stroke` | `str` | Stroke color |
| `stroke_width` | `int` | Stroke width |
| `stroke_dasharray` | `str` | Dash pattern |
| `label` | `str \| dict \| Component` | Label |
| `shape` | `Component` | Custom shape |

---

### 32. NEW: ReferenceDot
| Prop | Type | Description |
|------|------|-------------|
| `x` | `int \| str` | X position |
| `y` | `int \| str` | Y position |
| `r` | `int` | Radius |
| `x_axis_id` | `str \| int` | XAxis reference |
| `y_axis_id` | `str \| int` | YAxis reference |
| `if_overflow` | `str` | Overflow behavior |
| `fill` | `str` | Fill color |
| `stroke` | `str` | Stroke color |
| `stroke_width` | `int` | Stroke width |
| `label` | `str \| dict \| Component` | Label |
| `shape` | `Component` | Custom shape |

---

### 33. NEW: ErrorBar
| Prop | Type | Description |
|------|------|-------------|
| `data_key` | `str` | Error data key |
| `width` | `int` | Bar end width |
| `direction` | `"x" \| "y"` | Direction |
| `stroke` | `str` | Color |
| `stroke_width` | `int` | Line width |
| `is_animation_active` | `bool` | Animation |
| `animation_begin` | `int` | Animation delay |
| `animation_duration` | `int` | Duration |
| `animation_easing` | `str` | Easing |

---

### 34. NEW: Cell
| Prop | Type | Description |
|------|------|-------------|
| `fill` | `str` | Fill color |
| `stroke` | `str` | Stroke color |
| Any SVG props | `Any` | Standard SVG props |

---

### 35. NEW: LabelList
| Prop | Type | Description |
|------|------|-------------|
| `data_key` | `str` | Data key for values |
| `value_accessor` | `Callback` | Value accessor |
| `position` | `str` | Label position |
| `offset` | `int` | Position offset |
| `angle` | `int` | Rotation angle |
| `formatter` | `Callback` | Value formatter |
| `content` | `Component` | Custom content |
| `fill` | `str` | Text color |
| `font_size` | `int` | Font size |

---

### 36. NEW: Label
| Prop | Type | Description |
|------|------|-------------|
| `value` | `str \| int` | Label value |
| `position` | `str` | Position |
| `offset` | `int` | Offset |
| `angle` | `int` | Rotation angle |
| `formatter` | `Callback` | Value formatter |
| `content` | `Component` | Custom content |
| `fill` | `str` | Text color |
| `font_size` | `int` | Font size |

---

### 37. ChartTooltip Enhancements
**Current Props:** `content`, `cursor`, `hide_label`, `hide_indicator`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `active` | `bool` | Force active state |
| `default_index` | `int` | Default active index |
| `offset` | `int` | Offset from cursor |
| `position` | `dict` | Fixed position |
| `allow_escape_view_box` | `dict` | Allow overflow |
| `filter_null` | `bool` | Filter null values |
| `include_hidden` | `bool` | Include hidden series |
| `shared` | `bool` | Shared tooltip |
| `trigger` | `"hover" \| "click"` | Trigger type |
| `is_animation_active` | `bool \| "auto"` | Animation |
| `animation_begin` | `int` | Animation delay |
| `animation_duration` | `int` | Animation duration |
| `animation_easing` | `str` | Easing function |
| `axis_id` | `str \| int` | Axis reference |
| `wrapper_style` | `dict` | Wrapper styles |
| `content_style` | `dict` | Content styles |
| `item_style` | `dict` | Item styles |
| `label_style` | `dict` | Label styles |
| `separator` | `str` | Value separator |

---

### 38. ChartLegend Enhancements
**Current Props:** `content`, `vertical_align`

**Missing Props:**
| Prop | Type | Description |
|------|------|-------------|
| `layout` | `"horizontal" \| "vertical"` | Layout |
| `align` | `"left" \| "center" \| "right"` | Horizontal align |
| `icon_size` | `int` | Icon size |
| `icon_type` | `str` | Icon type |
| `payload` | `list[dict]` | Custom payload |
| `wrapper_style` | `dict` | Wrapper styles |
| `chart_width` | `int` | Chart width reference |
| `chart_height` | `int` | Chart height reference |
| `width` | `int` | Legend width |
| `height` | `int` | Legend height |
| `margin` | `dict` | Margins |
| `on_click` | `Callback` | Click handler |
| `on_mouse_enter` | `Callback` | Mouse enter |
| `on_mouse_leave` | `Callback` | Mouse leave |
| `formatter` | `Callback` | Value formatter |
| `item_sorter` | `str \| Callback` | Sort items |

---

## Implementation Priority

### Phase 1: Complete Existing Components (High Priority)
1. Add all missing props to existing chart types
2. Add animation props to all graphical elements
3. Add event handlers to all interactive components
4. Add axis reference props (`x_axis_id`, `y_axis_id`, etc.)

### Phase 2: Essential Missing Components (High Priority)
1. **ScatterChart + Scatter + ZAxis** - Common chart type
2. **ComposedChart** - Enables mixed charts
3. **ReferenceArea + ReferenceDot** - Important annotations
4. **Cell** - Required for custom coloring in Pie/Bar
5. **LabelList + Label** - Data labels
6. **ErrorBar** - Statistical visualization

### Phase 3: Advanced Charts (Medium Priority)
1. **FunnelChart + Funnel** - Business analytics
2. **Treemap** - Hierarchical data
3. **Sankey** - Flow visualization
4. **SunburstChart** - Hierarchical circular

### Phase 4: Enhanced Features (Lower Priority)
1. ChartTooltip advanced props
2. ChartLegend advanced props
3. Custom shapes/renderers
4. Gradient support (LinearGradient, RadialGradient)

---

## Summary Statistics

| Category | Count |
|----------|-------|
| Missing Chart Types | 6 |
| Missing Utility Components | 8 |
| Components Needing Prop Updates | 21 |
| Total Missing Props (estimated) | 200+ |