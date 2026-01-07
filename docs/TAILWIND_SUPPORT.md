# Refast Tailwind CSS Support

Refast provides an **optimized set** of Tailwind utility classes to balance flexibility with performance. For specific dimensions or custom values not listed here, use the `style` prop.

## ✅ Supported Utility Classes

### 1. Layout Structure
*   **Display**: `block`, `inline`, `flex`, `grid`, `hidden`, `table`.
*   **Sizing**: 
    *   `w-full`, `w-screen`, `w-auto`, `w-min`, `w-max`, `w-fit`.
    *   `h-full`, `h-screen`, `h-auto`, `h-min`, `h-max`, `h-fit`.
    *   `max-w-{size}`: `xs`, `sm`, `md`, `lg`, `xl`, `2xl`-`7xl`.
    *   `max-w-{keyword}`: `full`, `min`, `max`, `fit`, `prose`.
    *   `max-w-screen-{bp}`: `sm`, `md`, `lg`, `xl`, `2xl`.
*   **Flex**: `flex-row`, `flex-col`, `flex-wrap`, `flex-1`, `flex-none`, `grow`, `shrink`.
*   **Grid**: `grid-cols-1` to `6` and `12`, `col-span-*`, `row-span-*`.
*   **Alignment**: `justify-*`, `items-*`, `content-*`, `self-*` (start/end/center/between/around/stretch).
*   **Position**: `absolute`, `relative`, `fixed`, `sticky`.
*   **Z-Index**: `z-0`, `z-10`, `z-20`, `z-30`, `z-40`, `z-50`.
*   **Reset**: `top-0`, `left-0`, `right-0`, `bottom-0`, `inset-0`.

### 2. Spacing (Limited Scale)
Standard Tailwind spacing is supported for **0 to 6** (0 to 1.5rem), plus **8, 10, 12, 16**.
*   **Padding**: `p-*`, `px-*`, `py-*` (e.g., `p-4`, `px-6`).
*   **Margin**: `m-*`, `mx-*`, `my-*`.
*   **Gap**: `gap-0` to `gap-8`.

**Note:** For specific fixed width/heights (e.g. `w-64`, `h-10`), use `style={{ width: "16rem" }}`.

### 3. Typography
*   **Size**: `text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`, `text-3xl`.
*   **Weight**: `font-normal`, `font-medium`, `font-semibold`, `font-bold`.
*   **Align**: `text-left`, `text-center`, `text-right`, `text-justify`.
*   **Whitespace**: `whitespace-nowrap`, `whitespace-pre`, `whitespace-normal`.

### 4. Semantic Colors
We strictly support semantic tokens to ensure dark mode compatibility.
*   **Properties**: `bg-`, `text-`, `border-`, `ring-`.
*   **Tokens**: `primary`, `secondary`, `destructive`, `muted`, `accent`, `popover`, `card`, `background`, `foreground`, `input`, `border`.
*   **Variants**: `hover:` is available for bg/text/border. `focus:` is available for rings.

### 5. Visuals & Interaction
*   **Rounded**: `rounded`, `rounded-sm/md/lg/xl/2xl/3xl`, `rounded-full`, `rounded-none`. Also supports `rounded-t`, `rounded-l`, etc.
*   **Border Width**: `border`, `border-0`, `border-2`, `border-4`, `border-8`. Supports sides: `border-b-2`, `border-x`, etc.
*   **Shadow**: `shadow`, `shadow-sm`, `shadow-md`, `shadow-lg`, `shadow-xl`, `shadow-2xl`, `shadow-inner`.
*   **Cursor**: `cursor-pointer`, `cursor-not-allowed`, `cursor-text`, `cursor-move`.
*   **Outline**: `outline-none`.

---

## ⚠️ NOT Safelisted (Use `style` prop)

To keep the bundle size small (~1MB), the following are **NOT** included in the safelist and should be handled via the `style` prop:

1.  **Width / Height / Size** (`w-full`, `h-screen`, `w-64`, etc.)
    *   **Use**: `style={{ width: "100%" }}` or `style={{ width: "16rem" }}`
2.  **Specific Positioning** (`top-4`, `left-1/2`)
    *   **Use**: `style={{ top: "1rem" }}`
3.  **Opacity** (`opacity-50`)
    *   **Use**: `style={{ opacity: 0.5 }}`
4.  **Raw Colors** (`red-500`, `blue-600`)
    *   **Use**: Semantic tokens (preferred) or `style={{ color: "red" }}`.
5.  **Ordering**: `order-2`, `order-5` (Only `first`, `last`, `none` are valid classes).
