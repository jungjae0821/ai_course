import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: { port: 5173, strictPort: true },
  // 폴더 안의 다른 HTML(시안 등)을 훑지 않게 진입점을 고정한다.
  optimizeDeps: { entries: ['index.html'] },
});
