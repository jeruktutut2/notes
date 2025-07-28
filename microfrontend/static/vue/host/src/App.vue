<script setup>
    import { defineAsyncComponent } from 'vue'

    const RemoteButton = defineAsyncComponent(() =>
        import('remote/Button')
    )

    const RemoteText = defineAsyncComponent(() =>
        import('remote/Text')
    )
</script>

<template>
    <div>
        <RemoteButton />
        <RemoteText />
    </div>
</template>

<style scoped>
</style>
