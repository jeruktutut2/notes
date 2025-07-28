import { createMemoryHistory, createRouter } from 'vue-router'
import { loadRemote } from './loadRemote'
import { defineAsyncComponent } from 'vue'

// no need to put defineAsyncComponent, becouse component is async by default
const routes = [
    {
        path: "/",
        component: () => loadRemote('remote', 'http://localhost:3001', './AppView')
    },
    {
        path: "/about",
        component: () => loadRemote('remote', 'http://localhost:3001', './AboutView')
    },
    {
        path: "/profile",
        component: () => loadRemote('remote', 'http://localhost:3001', './ProfileView')
    }
]

const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

export default router