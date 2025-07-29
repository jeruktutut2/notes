<script setup>
    import { ref, onMounted } from 'vue'

    // let eventSource
    const eventSource = ref(null);

    onMounted(async () => {
        // const eventSource = new EventSource("http://localhost:8080/sse/handle-sse-without-channel");
        // const eventSource = new EventSource("/sse/handle-sse-without-channel");
        eventSource.value = new EventSource("/sse/handle-sse-without-channel-2?id=1");
        eventSource.value.onmessage = (event) => {
            console.log("SSE Data:", event.data);
            console.log("event:", event);
        }

        eventSource.value.onerror = (error) => {
            console.log("error:", error);
            eventSource.close();
        }
    })

    function close() {
      if (eventSource.value) {
        eventSource.value.close()
        eventSource.value = null
      }
    }
</script>

<template>
  <div>
    <button @click="close">close</button>
  </div>
</template>
