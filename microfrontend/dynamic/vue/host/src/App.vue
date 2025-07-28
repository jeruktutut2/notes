<script setup>
    import { defineAsyncComponent, markRaw, shallowRef } from 'vue'
    import { loadRemote } from './loadRemote'
    import { onMounted, ref } from 'vue'

    const RemoteButton = defineAsyncComponent(() => loadRemote('remote', './Button'))
    const RemoteText = defineAsyncComponent(() => loadRemote('remote', './Text'))

    const fetchCookie1 = async () => {
        try {
          const response = await fetch("/cookie/set-remote1", {
                method: 'GET'
          })
        } catch (error) {
            console.log("error:", error)
        }
    }

    const fetchCookie2 = async () => {
        try {
          const response = await fetch("/cookie/set-remote2", {
                method: 'GET'
          })
        } catch (error) {
            console.log("error:", error)
        }
    }

    const checkRemote = async () => {
        try {
          const response = await fetch("/remote/remoteEntry.js", {
                method: 'GET'
          })
        } catch (error) {
            console.log("error:", error)
        }
    }

    onMounted(async () => {
        await fetchCookie1()
        try {
            // RemoteButton.value = defineAsyncComponent(() => loadRemote('remote', 'http://localhost:8080', './Button'))
            // RemoteText = defineAsyncComponent(() => loadRemote('remote', 'http://localhost:8080', './Text'))
            // RemoteButton.value = defineAsyncComponent(() => loadRemote('remote', './Button'))
            // RemoteButton.value = markRaw(await loadRemote('remote', './Button'))
            // RemoteText.value = markRaw(await loadRemote('remote', './Text'))
            // console.log("RemoteButton.value:", RemoteButton.value)
            // RemoteButton.value = remoteButton
            // RemoteButton = defineAsyncComponent(() => loadRemote('remote', './Button'))
            // RemoteText = defineAsyncComponent(() => loadRemote('remote', './Text'))
        } catch (error) {
            console.log("error:", error)
        }
    })
</script>

<template>
    <div class="hidden bg-red-500 text-white p-4"></div>
    <!-- <div>
        <button class="bg-blue-500 text-white px-4 py-2 rounded" @click="fetchCookie1">SetCookie1</button>
        <button class="bg-blue-500 text-white px-4 py-2 rounded" @click="fetchCookie2">SetCookie2</button>
    </div> -->
    <Suspense>
        <template #default>
            <div>
                <RemoteButton :key="'remote-button'" />
            </div>
        </template>
        <template #fallback>
            <div>Loading remote...</div>
        </template>
    </Suspense>
    <Suspense>
        <template #default>
            <div>
                <RemoteText :key="'remote-text'"/>
            </div>
        </template>
        <template #fallback>
            <div>Loading remote...</div>
        </template>
    </Suspense>
    <p>
        <strong>Current route path:</strong> {{ $route.fullPath }}
    </p>
    <nav>
        <RouterLink to="/">App </RouterLink>
        <RouterLink to="/about">About </RouterLink>
        <RouterLink to="/profile">Profile </RouterLink>
    </nav>
    <main>
        <RouterView />
    </main>
</template>

<style scoped>
</style>
