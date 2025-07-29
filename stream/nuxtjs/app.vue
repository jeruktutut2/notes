<script setup>
    import { ref, onMounted } from 'vue'

    const message = ref('Hello Nuxt!')

    onMounted(async () => {
        console.log('UI telah selesai dirender di browser')

        const response = await fetch("http://localhost:8080/stream/stream-without-channel"); // Panggil endpoint backend
        // const response = await fetch("/stream/stream-without-channel");
        if (!response.body) throw new Error("Response body is empty");
        const reader = response.body.getReader();
        const decoder = new TextDecoder();
    
        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
    
            const chunk = decoder.decode(value, { stream: true });
            console.log("chunk:", chunk);
        }
    })

</script>

<template>
    <div>
        <NuxtRouteAnnouncer />
        <NuxtWelcome />
    </div>
</template>

<style>

</style>