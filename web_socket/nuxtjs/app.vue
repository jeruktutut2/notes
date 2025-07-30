<script setup>
  import { ref, onBeforeUnmount } from "vue";

  const ws = ref(null);
  const clientId = ref("");
  const clientIdSendTo = ref("")
  const message = ref("");
  const messages = ref([]);

  function connect() {
    if (!clientId.value) {
      alert("Masukkan ID dulu!");
      return;
    }

    if (ws.value) {
      ws.value.close();
    }

    ws.value = new WebSocket(`ws://localhost:8080/ws?id=${clientId.value}`);
    // ws.value = new WebSocket(`/ws?id=${clientId.value}`);

    ws.value.onopen = () => {
      console.log(`Terhubung sebagai ${clientId.value}`);
    };

    ws.value.onmessage = (event) => {
      messages.value.push(event.data);
    };

    ws.value.onclose = () => {
      console.log("WebSocket terputus");
    };
  }

  async function sendMessage() {
    if (!ws.value || ws.value.readyState !== WebSocket.OPEN) {
      alert("WebSocket belum terhubung!");
      return;
    }

    await fetch(`http://localhost:8080/send-message?clientIdSendTo=${clientIdSendTo.value}&msg=${message.value}`);
    // await fetch(`/send-message?clientIdSendTo=${clientIdSendTo.value}&msg=${message.value}`);
    messages.value.push(`Anda: ${message.value}`);
  }

  onBeforeUnmount(() => {
    if (ws.value) {
      ws.value.close();
    }
  });
</script>
<template>
  <div>
    <!-- <NuxtRouteAnnouncer /> -->
    <!-- <NuxtWelcome /> -->
    <h1>WebSocket Client (Nuxt.js)</h1>

    <input v-model="clientId" placeholder="Masukkan ID Anda" />
    <button @click="connect">Hubungkan</button>

    <input v-model="clientIdSendTo" placeholder="Masukkan ID Send To Anda" />
    <!-- <button @click="connect">Hubungkan</button> -->

    <input v-model="message" placeholder="Ketik pesan..." />
    <button @click="sendMessage">Kirim</button>

    <div class="messages">
      <h3>Pesan:</h3>
      <ul>
        <li v-for="(msg, index) in messages" :key="index">
          {{ msg }}
        </li>
      </ul>
    </div>
  </div>
</template>
