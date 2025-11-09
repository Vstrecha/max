import { fileURLToPath, URL } from 'node:url'

import { defineConfig, ViteDevServer } from 'vite'

import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import morgan from 'morgan'

// https://vite.dev/config/
export default defineConfig(() => {
  return {
    plugins: [morganPlugin(), vue(), vueDevTools()],
    server: {
      allowedHosts: ['horseshoe-crab.ru', 'localhost', 'max-total.ru'],
    },
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
  }
})

function morganPlugin() {
  return {
    name: 'morgan-plugin',
    configureServer(server: ViteDevServer) {
      server.middlewares.use(morgan('common'))
    },
  }
}
