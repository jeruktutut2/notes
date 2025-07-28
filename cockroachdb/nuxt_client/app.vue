<script setup>
    import { ref } from 'vue'
    import { HomeIcon, AcademicCapIcon, XMarkIcon, Bars3Icon } from '@heroicons/vue/24/outline'

    const isMenuOpen = ref(false)
</script>
<template>
    <div class="flex min-h-screen">
        <!-- <NuxtRouteAnnouncer /> -->
        <!-- <NuxtWelcome /> -->
        <!-- <div class="flex"> -->
            <aside :class="[
                    'w-[250px] p-4 border border-gray-400',
                    'md:block',
                    isMenuOpen ? 'block' : 'hidden'
                ]">
                 <nav>
                    <ul class="space-y-2">
                        <li>
                            <NuxtLink to="/show" class="block border p-2 hover:bg-gray-100 flex items-center gap-2 dark:hover:bg-gray-700 dark:text-white dark:border-gray-">
                                <AcademicCapIcon class="h-5 w-5" />
                                Show
                            </NuxtLink>
                        </li>
                    </ul>
                 </nav>
            </aside>
            <main class="border border-gray-400 flex-1 flex flex-col">
                <header class="border border-gray-400 p-4 flex justify-between items-center">
                    <!-- <span>Header</span> -->
                    <button class="md:hidden" @click="isMenuOpen = !isMenuOpen">
                        <component :is="isMenuOpen ? XMarkIcon : Bars3Icon" class="h-6 w-6" />
                    </button>
                    <span>Header</span>
                </header>
                <div class="border border-gray-400 flex-1">
                    <h1>main</h1>
                </div>
                <footer class="border border-gray-400 p-4">
                    <h1>footer</h1>
                </footer>
            </main>
        <!-- </div> -->
        <!-- <header class="border border-gray-400 p-4 flex justify-between items-center">
            <span>Header</span>
            <button class="md:hidden" @click="isMenuOpen = !isMenuOpen">
                <component :is="isMenuOpen ? XMarkIcon : Bars3Icon" class="h-6 w-6" />
            </button>
        </header> -->
        <!-- <div class="flex flex-1 flex-col md:flex-row">
            <aside :class="[
                    'md:w-1/4 p-4 border border-gray-400',
                    'md:block',
                    isMenuOpen ? 'block' : 'hidden'
                ]">
                 <nav>
                    <ul class="space-y-2">
                        <li>
                            <NuxtLink to="/show" class="block border p-2 hover:bg-gray-100 flex items-center gap-2 dark:hover:bg-gray-700 dark:text-white dark:border-gray-">
                                <AcademicCapIcon class="h-5 w-5" />
                                Show
                            </NuxtLink>
                        </li>
                    </ul>
                 </nav>
            </aside>
            <main class="border border-gray-400 flex-1 flex flex-col">
                <div class="border border-gray-400 flex-1">
                    <h1>main</h1>
                </div>
                <footer class="border border-gray-400 p-4">
                    <h1>footer</h1>
                </footer>
            </main>
        </div> -->
        <!-- <footer class="border borger-gray-400 p-4">
            <h1>footer</h1>
        </footer> -->
    </div>
</template>
