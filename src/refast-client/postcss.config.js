export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
    // Optimise CSS output — dedupe rules, collapse shorthand, etc.
    ...(process.env.NODE_ENV === 'production' ? { cssnano: { preset: 'default' } } : {}),
  },
};
