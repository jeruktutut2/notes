<script setup>
    import Button from './components/Button.vue'
    import Text from './components/Text.vue'
    import AppView from './views/AppView.vue'
    import AboutView from './views/AboutView.vue'
    import ProfileView from './views/ProfileView.vue'
</script>

<template>
    <Button />
    <Text />
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
