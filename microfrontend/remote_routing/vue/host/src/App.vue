<script setup>
</script>

<template>
    <p>
        <strong>Current Host route path:</strong> {{ $route.fullPath }}
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
