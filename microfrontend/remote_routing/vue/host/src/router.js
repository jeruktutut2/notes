import { createMemoryHistory, createRouter } from 'vue-router'

const AppRemoteView = () => import("remote/AppView")
const AboutRemoteView = () => import("remote/AboutView")
const ProfileRemoteView = () => import("remote/ProfileView")

const routes = [
    {
        path: "/",
        component: AppRemoteView
    },
    {
        path: "/about",
        component: AboutRemoteView
    },
    {
        path: "/profile",
        component: ProfileRemoteView
    }
]

const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

export default router