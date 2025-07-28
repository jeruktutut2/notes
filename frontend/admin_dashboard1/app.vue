<script setup>
    // import { ref, onMounted, onBeforeUnmount } from 'vue'
    // import { HomeIcon, AcademicCapIcon, XMarkIcon, Bars3Icon } from '@heroicons/vue/24/outline'

    // const isAsideOpen = ref(false)
    // const isMobile = ref(false)

    // const handleResize = () => {
    //     isMobile.value = window.innerWidth < 1024
    //     // console.log("isMobile.value:",isMobile.value)
    //     if (!isMobile.value) {
    //         isAsideOpen.value = true
    //     } else {
    //         isAsideOpen.value = false
    //     }
    //     // console.log("isMobile.value:",isMobile.value, "isAsideOpen.value:",isAsideOpen.value)
    //     // isAsideOpen.value = true 
    // }

    // const toggleAside = () => {
    //     isAsideOpen.value = !isAsideOpen.value
    // }

    // const closeOverlay = () => {
    //     isAsideOpen.value = false
    // }

    // onMounted(() => {
    //     handleResize()
    //     window.addEventListener("resize", handleResize);
    // })

    // onBeforeUnmount(() => {
    //     window.removeEventListener("resize", handleResize)
    // })
</script>
<template>
    <!-- <div class="min-h-screen flex">
        <div class="fixed inset-0 bg-black bg-opacity-30 z-1" 
            v-if="isAsideOpen && isMobile"
            @click="closeOverlay">
        </div>
        <aside :class="[
                'min-h-screen bg-white w-64 fixed lg:static flex flex-col border-r',
                isMobile
                    ? (isAsideOpen ? 'translate-x-0' : '-translate-x-full')
                    : (isAsideOpen ? 'block' : 'hidden')
            ]">
            <div class="h-[56px] flex items-center p-2 border-b">
                <NuxtLink class="flex items-center">
                    <NuxtImg src="https://placehold.co/32x32" class="w-8 h-8 mr-2" />
                    <span>LOGO</span>
                </NuxtLink>
            </div>
            <div class="min-h-[calc(100vh-110px)]">
                <nav>
                    <ul class="space-y-2">
                        <li>
                            <NuxtLink to="/show" class="block p-2 hover:bg-gray-100 flex items-center gap-2">
                                <AcademicCapIcon class="h-5 w-5" />
                                Show
                            </NuxtLink>
                        </li>
                    </ul>
                </nav>
            </div>
            <div class="h-[56px] border-t">footer</div>
        </aside>
        <main class="flex-1 min-h-screen flex flex-col">
            <header class="h-[56px] flex border-b">
                <button class="px-1" @click="toggleAside"><Bars3Icon class="h-6 w-6" />
                </button>
                <div class="">user</div>
            </header>
            <div class="min-h-[calc(100vh-110px)]">
                <h1 class="text-2xl font-bold mb-6">Dashboard</h1>
                <div class="grid grid-clos-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
                    <div class="border rounded-xl p-4 bg-white">Card 1</div>
                    <div class="border rounded-xl p-4 bg-white">Card 2</div>
                    <div class="border rounded-xl p-4 bg-white">Card 3</div>
                </div>
                <div class="border rounded-xl p-4 bg-white h-64">Tempat chart atau grafik</div>
            </div>
            <footer class="h-[56px] border-t">Footer</footer>
        </main>
    </div> -->
    <NuxtPage />
</template>
