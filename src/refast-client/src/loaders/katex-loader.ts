/**
 * Lazy KaTeX loader — this file is ONLY ever dynamically imported.
 *
 * Keeping remark-math / rehype-katex / katex in a dedicated module that is
 * never statically imported anywhere ensures the bundler cannot create a
 * static import edge from the main bundle (or vendor chunk) to the katex
 * chunk.  The entire katex dependency tree is fetched only when this module
 * is explicitly imported at runtime.
 *
 * The KaTeX CSS is injected as a <style> side-effect so it is included
 * only when LaTeX rendering is actually needed.
 */
export { default as remarkMath } from 'remark-math';
export { default as rehypeKatex } from 'rehype-katex';

import katexCss from 'katex/dist/katex.min.css?inline';

if (typeof document !== 'undefined' && !document.getElementById('refast-katex-css')) {
  const style = document.createElement('style');
  style.id = 'refast-katex-css';
  style.textContent = katexCss;
  document.head.appendChild(style);
}
