import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'

import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig(() => {
  return {
    base:  '/',
    plugins: [vue()],
    server: {
      allowedHosts: ['horseshoe-crab.ru', 'localhost', 'host.docker.internal'],
    },
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
  }
})
