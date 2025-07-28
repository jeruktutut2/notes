import { createMemoryHistory, createRouter, createWebHistory } from 'vue-router'
import { loadRemote } from './loadRemote'
import App from './App.vue'

// no need to put defineAsyncComponent, becouse component is async by default
const routes = [
    // {
    //     path: "/",
    //     component: App
    // },
    {
        path: "/",
        component: () => loadRemote('remote', './AppView')
    },
    {
        path: "/about",
        component: () => loadRemote('remote', './AboutView')
    },
    {
        path: "/profile",
        component: () => loadRemote('remote', './ProfileView')
    }
]

const router = createRouter({
    // history: createMemoryHistory(),
    history: createWebHistory(),
    routes,
})

export default router