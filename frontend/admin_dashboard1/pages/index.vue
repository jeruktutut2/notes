<script setup>
    import { ref, onMounted, onBeforeUnmount } from 'vue'
    import { HomeIcon, AcademicCapIcon, XMarkIcon, Bars3Icon } from '@heroicons/vue/24/outline'

    const isAsideOpen = ref(false)
    const isMobile = ref(false)
    const isDark = ref(false)

    const handleResize = () => {
        isMobile.value = window.innerWidth < 1024
        // console.log("isMobile.value:",isMobile.value)
        if (!isMobile.value) {
            isAsideOpen.value = true
        } else {
            isAsideOpen.value = false
        }
        // console.log("isMobile.value:",isMobile.value, "isAsideOpen.value:",isAsideOpen.value)
        // isAsideOpen.value = true 
    }

    const toggleAside = () => {
        isAsideOpen.value = !isAsideOpen.value
    }

    const closeOverlay = () => {
        isAsideOpen.value = false
    }

    const toggleDark = () => {
        isDark.value = !isDark.value
        document.documentElement.classList.toggle("dark", isDark.value)
    }

    onMounted(() => {
        handleResize()
        window.addEventListener("resize", handleResize);
        isDark.value = document.documentElement.classList.contains("dark")
    })

    onBeforeUnmount(() => {
        window.removeEventListener("resize", handleResize)
    })
</script>
<template>
    <div class="min-h-screen flex text-neutral-700 dark:text-neutral-100">
        <!-- <NuxtRouteAnnouncer /> -->
        <!-- <NuxtWelcome /> -->
        <div class="fixed inset-0 bg-black bg-opacity-30 z-1" 
            v-if="isAsideOpen && isMobile"
            @click="closeOverlay">
        </div>
        <aside :class="[
                'min-h-screen w-64 fixed lg:static flex flex-col',
                'bg-white dark:bg-neutral-900',
                // isAsideOpen ? 'block' : 'hidden'
                isMobile
                    ? (isAsideOpen ? 'translate-x-0' : '-translate-x-full')
                    : (isAsideOpen ? 'block' : 'hidden')
            ]">
            <div :class="['h-[56px] flex items-center gap-2 px-4 py-3 font-bold text-lg', 
            'border-b border-neutral-100 dark:border-neutral-600']">
                <NuxtLink class="flex items-center">
                    <NuxtImg src="https://placehold.co/32x32" class="w-8 h-8 mr-2" />
                    <span>LOGO</span>
                </NuxtLink>
            </div>
            <div :class="['min-h-[calc(100vh-110px)] border-neutral-100']">
                <nav>
                    <ul class="space-y-2">
                        <li>
                            <NuxtLink to="/" :class="['block p-2 flex items-center gap-3 px-3 py-2',
                                'hover:bg-neutral-200 hover:dark:bg-neutral-600 text-neutral-700 dark:text-white hover:text-black',
                                'transition']"
                                active-class="bg-neutral-800 text-black font-semibold"
                                exact-active-class="bg-gray-200 text-black font-semibold">
                                <AcademicCapIcon class="h-5 w-5" />
                                /
                            </NuxtLink>
                            <NuxtLink to="/h" :class="['block p-2 flex items-center gap-3 px-3 py-2',
                                'hover:bg-neutral-200 hover:dark:bg-neutral-600 text-neutral-700 dark:text-white hover:text-black',
                                'transition']">
                                <AcademicCapIcon class="h-5 w-5" />
                                H
                            </NuxtLink>
                            <NuxtLink to="/w" :class="['block p-2 flex items-center gap-3 px-3 py-2',
                                'hover:bg-neutral-200 hover:dark:bg-neutral-600 text-neutral-700 dark:text-white hover:text-black',
                                'transition']">
                                <AcademicCapIcon class="h-5 w-5" />
                                W
                            </NuxtLink>
                            <NuxtLink to="/dashboard1" :class="['block p-2 flex items-center gap-3 px-3 py-2',
                                'hover:bg-neutral-200 hover:dark:bg-neutral-600 text-neutral-700 dark:text-white hover:text-black',
                                'transition']">
                                <AcademicCapIcon class="h-5 w-5" />
                                dashboard1
                            </NuxtLink>
                            <NuxtLink to="/dashboard2" :class="['block p-2 flex items-center gap-3 px-3 py-2',
                                'hover:bg-neutral-200 hover:dark:bg-neutral-600 text-neutral-700 dark:text-white hover:text-black',
                                'transition']">
                                <AcademicCapIcon class="h-5 w-5" />
                                dashboard2
                            </NuxtLink>
                            <NuxtLink to="/padding-margin" :class="['block p-2 flex items-center gap-3 px-3 py-2',
                                'hover:bg-neutral-200 hover:dark:bg-neutral-600 text-neutral-700 dark:text-white hover:text-black',
                                'transition']">
                                <AcademicCapIcon class="h-5 w-5" />
                                padding-margin
                            </NuxtLink>
                            <NuxtLink to="/positioning-with-grid" :class="['block p-2 flex items-center gap-3 px-3 py-2',
                                'hover:bg-neutral-200 hover:dark:bg-neutral-600 text-neutral-700 dark:text-white hover:text-black',
                                'transition']">
                                <AcademicCapIcon class="h-5 w-5" />
                                positioning-with-grid
                            </NuxtLink>
                            <NuxtLink to="/positioning" :class="['block p-2 flex items-center gap-3 px-3 py-2',
                                'hover:bg-neutral-200 hover:dark:bg-neutral-600 text-neutral-700 dark:text-white hover:text-black',
                                'transition']">
                                <AcademicCapIcon class="h-5 w-5" />
                                positioning
                            </NuxtLink>
                            <NuxtLink to="/transform" :class="['block p-2 flex items-center gap-3 px-3 py-2',
                                'hover:bg-neutral-200 hover:dark:bg-neutral-600 text-neutral-700 dark:text-white hover:text-black',
                                'transition']">
                                <AcademicCapIcon class="h-5 w-5" />
                                transform
                            </NuxtLink>
                            <NuxtLink to="/transition" :class="['block p-2 flex items-center gap-3 px-3 py-2',
                                'hover:bg-neutral-200 hover:dark:bg-neutral-600 text-neutral-700 dark:text-white hover:text-black',
                                'transition']">
                                <AcademicCapIcon class="h-5 w-5" />
                                transition
                            </NuxtLink>
                        </li>
                    </ul>
                </nav>
            </div>
            <div class="h-[56px] border-t border-r-2 border-neutral-100 dark:border-neutral-600">footer</div>
        </aside>
        <main :class="['flex-1 min-h-screen flex flex-col']">
            <header :class="['h-[56px] flex items-center', 
            'border-b border-neutral-100 dark:border-neutral-600 bg-white dark:bg-neutral-800']">
                <button class="px-1" @click="toggleAside"><Bars3Icon class="h-6 w-6" />
                    <!-- <component :is="isAsideOpen ? XMarkIcon : Bars3Icon" class="h-6 w-6" /> -->
                </button>
                <div class="">user</div>
                <button @click="toggleDark" :class="['p-2 rounded', 'bg-neutral-200 dark:bg-neutral-700', 'text-neutral-800 dark:text-neutral-200']">
                    {{ isDark ? '🌙 Dark' : '☀️ Light' }}
                </button>
            </header>
            <div class="min-h-[calc(100vh-110px)] bg-neutral-100 dark:bg-neutral-800">
                <h1 class="text-2xl font-bold mb-6">Dashboard</h1>
                <div class="grid grid-clos-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
                    <div class="border dark:border-neutral-600 rounded-xl p-4 dark:bg-neutral-900">Card 1</div>
                    <div class="border rounded-xl p-4 bg-white">Card 2</div>
                    <div class="border rounded-xl p-4 bg-white">Card 3</div>
                </div>
                <div class="border border-neutral-100 dark:border-neutral-600 rounded-xl p-4 bg-white h-64">Tempat chart atau grafik</div>
            </div>
            <footer class="h-[56px] border-t border-neutral-100 dark:border-neutral-600 bg-white dark:bg-neutral-700">Footer</footer>
        </main>
    </div>
</template>