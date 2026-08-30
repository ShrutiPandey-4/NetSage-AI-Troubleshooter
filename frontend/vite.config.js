import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Keep optimized dependencies in Vite's project-local default cache.
export default defineConfig({
  plugins: [react()],
  cacheDir: 'node_modules/.vite',
});
