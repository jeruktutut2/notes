import { createApp } from 'vue'
import './style.css'
import "./index.css"
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'
import ComponentA from "./components/ComponentA.vue"
import ComponentB from "./components/ComponentB.vue"
import ComponentC from "./components/ComponentC.vue"

const router = createRouter({
    routes: [
        {
            path: "/component-a",
            component: ComponentA
        },
        {
            path: "/component-b",
            component: ComponentB
        },
        {
            path: "/component-c",
            component: ComponentC
        }
    ],
    history: createWebHistory()
})

router.beforeEach((to, from, next) => {
    console.info(`before navigation to ${to.fullPath} from ${from.fullPath}`)
    next();
})

router.afterEach((to, from) => {
    console.info(`after navigation to ${to.fullPath} from ${from.fullPath}`)
})

createApp(App).use(router).mount('#app')
