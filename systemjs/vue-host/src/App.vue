<script setup>
// import HelloWorld from './components/HelloWorld.vue'
  import { ref, onMounted, markRaw } from 'vue'
  // import SystemJS from 'systemjs'
  // import * as SystemJS from 'systemjs'
  import Fallback from "./components/Fallback.vue"

  // SystemJS.import('http://localhost:4173/vue-remote.umd.cjs').then((mod) => {
  //   const { ComponentA, ComponentB, ComponentC } = mod;
  // })
  // const componentA = ref(Fallback)
  const componentA = ref(markRaw(Fallback))
  const componentB = ref(null)
  const componentC = ref(null)
  onMounted(async () => {
    try {
      // const mod = await SystemJS.import('http://localhost:4173/vue-remote.umd.cjs')
      const mod = await System.import('http://localhost:4173/vue-remote.umd.js')
      // componentA.value = mod.ComponentA
      componentA.value = markRaw(mod.ComponentA)
      // componentB.value = mod.ComponentB
      componentB.value = markRaw(mod.ComponentB)
      // componentC.value = mod.ComponentC
      componentC.value = markRaw(mod.ComponentC)
    } catch(e) {
      console.log("e:", e)
    }
  })
</script>

<template>
  <!-- <div>
    <a href="https://vite.dev" target="_blank">
      <img src="/vite.svg" class="logo" alt="Vite logo" />
    </a>
    <a href="https://vuejs.org/" target="_blank">
      <img src="./assets/vue.svg" class="logo vue" alt="Vue logo" />
    </a>
  </div> -->
  <!-- <HelloWorld msg="Vite + Vue" /> -->
  <h1 class="bg-blue-500 text-5xl">Root</h1>
  <RouterView/>

  <component :is="componentA" v-if="componentA" />
  <component :is="componentB" v-if="componentB" />
  <component :is="componentC" v-if="componentC" />
</template>

<style scoped>
/* .logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
} */
</style>
