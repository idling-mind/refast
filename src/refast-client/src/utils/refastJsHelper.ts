/**
 * Helper object injected into JavaScript execution contexts (ctx.js() and ctx.call_js()).
 *
 * Provides a bridge for JavaScript code to invoke Python callbacks and emit events.
 * Available as the `refast` parameter inside JS code.
 *
 * Usage from ctx.js():
 * ```python
 * async def handle_enter(ctx: Context):
 *     ctx.state.set("submitted", True)
 *     await ctx.refresh()
 *
 * Input(
 *     on_keydown=ctx.js(
 *         """
 *         if (event.key === 'Enter') {
 *             refast.invoke(args.on_enter);
 *         }
 *         """,
 *         on_enter=ctx.callback(handle_enter)
 *     )
 * )
 * ```
 */

/**
 * Shape of a serialized callback reference passed as a bound arg.
 */
interface SerializedCallback {
  callbackId: string;
  boundArgs?: Record<string, unknown>;
  props?: string[];
}

/**
 * The refast helper object available in JS execution contexts.
 */
export interface RefastJsHelper {
  /**
   * Invoke a Python callback from JavaScript.
   *
   * @param callback - A serialized callback reference (passed via bound args).
   *   This is a ctx.callback() object passed as a bound arg to ctx.js().
   * @param data - Optional data to send with the callback. These become
   *   keyword arguments in the Python callback function.
   *
   * @example
   * ```python
   * # Python side
   * Input(
   *     on_keydown=ctx.js(
   *         "if (event.key === 'Enter') { refast.invoke(args.on_submit, { value: event.value }); }",
   *         on_submit=ctx.callback(handle_submit)
   *     )
   * )
   * ```
   */
  invoke: (callback: SerializedCallback, data?: Record<string, unknown>) => void;
}

/**
 * Singleton helper instance injected into all JS execution contexts.
 * Dispatches the `refast:callback` CustomEvent that EventManager listens for.
 */
export const refastJsHelper: RefastJsHelper = {
  invoke(callback: SerializedCallback, data: Record<string, unknown> = {}) {
    if (!callback || !callback.callbackId) {
      console.warn('[Refast] refast.invoke() called with invalid callback:', callback);
      return;
    }

    const event = new CustomEvent('refast:callback', {
      detail: {
        callbackId: callback.callbackId,
        data: { ...(callback.boundArgs || {}), ...data },
      },
    });
    window.dispatchEvent(event);
  },
};
