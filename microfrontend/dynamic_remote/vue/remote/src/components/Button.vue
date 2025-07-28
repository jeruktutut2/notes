<script setup>
    const log = async () => {
        console.log("console log from remote vue")
    }
</script>

<template>
    <div>
        <button class="bg-blue-500 text-white px-4 py-2 rounded" @click="log">Button</button>
    </div>
</template>