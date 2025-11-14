import './assets/main.css'
import 'vant/lib/index.css'
import 'animate.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router/router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.mount('#app')

// window.onerror = function (message, source, lineno, colno, error) {
//   const logMessage = `Ошибка: ${message} в ${source}:${lineno}:${colno}`

//   alert(logMessage)
// }
