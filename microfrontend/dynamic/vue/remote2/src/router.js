import { createMemoryHistory, createRouter, createWebHistory } from 'vue-router'
import AppView from "./views/AppView.vue"
import AboutView from "./views/AboutView.vue"
import ProfileView from "./views/ProfileView.vue"

const routes = [
    {
        path: "/",
        component: AppView
    },
    {
        path: "/about",
        component: AboutView
    },
    {
        path: "/profile",
        component: ProfileView
    }
]

const router = createRouter({
    // history: createMemoryHistory(),
    history: createWebHistory(),
    routes,
})

export default router