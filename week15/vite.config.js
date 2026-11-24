import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [react(), tailwindcss()],
  // GitHub Pages 하위 경로(/ai_course/week15/dist/)에서도 열리도록 상대 경로로 빌드한다.
  base: './',
  server: { port: 5173, strictPort: true },
  // 폴더 안의 다른 HTML(시안 등)을 훑지 않게 진입점을 고정한다.
  optimizeDeps: { entries: ['index.html'] },
});
