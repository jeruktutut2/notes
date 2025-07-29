<script setup>
    import { ref } from 'vue'
    
    const requestId = ref("")

    const GetRequestId = async () =>  {
        try {
            const response = await fetch("/request-id")
            const json = await response.json()
            requestId.value = json?.data?.requestId ?? "failed getting requestId"
            // console.log("mantap")
        } catch(e) {
            requestId.value = "an error has accoured"
            console.log("e:", e)
        }
      }
</script>
<template>
    <div class="flex flex-col items-center justify-center h-screen">
    <!-- <NuxtRouteAnnouncer /> -->
    <!-- <NuxtWelcome /> -->
        <p class="mb-4 text-large text-lg font-medium text-gray-700">{{ requestId || "No request id" }}</p>
        <button class="px-6 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition" @click="GetRequestId">GET REQUEST ID</button>
    </div>
</template>
