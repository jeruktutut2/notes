import { createApp } from 'vue'
import './style.css'
import "./index.css"
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import Hello from "./components/HelloWorld.vue"

const router = createRouter({
    routes: [
        {
            path: "/",
            component: Hello
        }
    ],
    history: createWebHistory()
})

createApp(App).use(router).mount('#app')
