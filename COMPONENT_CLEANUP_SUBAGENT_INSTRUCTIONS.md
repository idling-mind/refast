# Component Cleanup Subagent Instructions

## Objective
Standardize, clean up, and document all components across the Refast Python backend (`src/refast/components/`) and React frontend (`src/refast-client/src/components/`). Ensure identical structures, consistent props (e.g., `variant`, `size`), and thorough documentation.

## Core Principles
1. **No Backward Compatibility Required**: Prioritize clean, legible, and maintainable code over preserving old APIs.
2. **Alignment**: Python kwargs and React props must match exactly (with `snake_case` in Python corresponding to `camelCase` in React).
3. **Consistency**: Options like `variant`, `size`, `color`, etc., must be identical across all applicable components. Use Literal types in Python to enforce these.
4. **Grouped Documentation**: Components that go together (e.g., Sidebar and its subcomponents, ToggleGroups and Toggles, CheckboxGroups and Checkboxes) MUST be documented together in the same chapter/file.
5. **Testing**: Cleanup any tests that break due to API changes.

## Step-by-Step Task Execution

For each component group assigned to you:

### 1. Python Implementation (`src/refast/components/shadcn/`)
- Review the component class.
- Standardize the `__init__` arguments.
  - Require specific types (e.g., `Literal["default", "destructive", "outline"]`).
  - Set sensible defaults.
- Add comprehensive docstrings for the class and its arguments.
- Ensure the `render` method correctly serializes the props.
- Remove unnecessary wrapper code or dead code.

### 2. React Implementation (`src/refast-client/src/components/shadcn/`)
- Review the React component interface.
- Ensure the interface strictly matches the Python output (handling camelCase conversion naturally).
- Standardize Tailwind classes relying on the defined variants/sizes using `cva` or similar patterns if present.
- Strip out unused or bloated code.

### 3. Documentation (`docs_site/pages/components/`)
- Find the corresponding documentation file or create it.
- Document the entire set of related components together.
- Include Python code examples and rendered live demos.
- Explicitly list the available props, variants, and sizes.

### 4. Tests (`tests/`)
- Locate tests for the assigned components (e.g., `tests/unit/test_components.py`).
- Fix any broken tests resulting from prop standardizations.
- Remove tests for deprecated/removed features.

## Output
When reporting back, summarize:
1. Components modified (Python & React).
2. Props standardized (variants, sizes, etc.).
3. Documentation file updated.
4. Test files fixed.
