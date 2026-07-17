export type ComponentSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';

export const STANDARD_ICON_SIZES: Record<ComponentSize, number> = {
  xs: 12,
  sm: 14,
  md: 16,
  lg: 20,
  xl: 24,
};

/**
 * Returns the default icon size (in pixels) for a given component size.
 */
export function getIconSize(size?: ComponentSize, defaultSize: number = 16): number {
  if (!size) return defaultSize;
  return STANDARD_ICON_SIZES[size] ?? defaultSize;
}
