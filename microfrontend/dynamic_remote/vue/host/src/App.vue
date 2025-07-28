<script setup>
    import { defineAsyncComponent } from 'vue'
    import { loadRemote } from './loadRemote'
    
    const RemoteButton = defineAsyncComponent(() => loadRemote('remote', 'http://localhost:3001', './Button'))
    const RemoteText = defineAsyncComponent(() => loadRemote('remote', 'http://localhost:3001', './Text'))
</script>

<template>
  <!-- <HelloWorld msg="Vite + Vue" /> -->
    <!-- <input type="text" placeholder="text" class="p-3 m-3" /> -->
    <!-- <div>
        <button class="bg-blue-500 text-white px-4 py-2 rounded">Button Host</button>
    </div> -->
    <RemoteButton />
    <RemoteText />
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
