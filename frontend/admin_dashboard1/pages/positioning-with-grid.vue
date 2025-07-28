<script setup>
</script>
<template>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-5 gap-4 p-6">
    <!-- Static -->
    <div class="bg-gray-200 p-4 border">
      <p class="text-sm font-semibold">Static (default) tidak bisa diposisikan dengan top/right dll.</p>
      <div class="static bg-white p-2 mt-2">Box Static</div>
    </div>

    <!-- Relative -->
    <div class="bg-gray-200 p-4 border">
      <p class="text-sm font-semibold">Relative hanya membuat referensi untuk anak absolute.</p>
      <div class="relative bg-white p-2 mt-2">Box Relative</div>
    </div>

    <!-- Absolute -->
    <div class="bg-gray-200 p-4 border relative h-[100px] overflow-hidden">
      <p class="text-sm font-semibold">Absolute (posisi dalam box) mengambang dalam parent yang relative.</p>
      <div class="absolute top-2 right-2 bg-blue-500 text-white px-2 py-1 text-xs">ABS</div>
    </div>

    <!-- Fixed -->
    <div class="bg-gray-200 p-4 border">
      <p class="text-sm font-semibold">Fixed (selalu di layar) tetap di pojok layar walau scroll.</p>
      <div class="fixed bottom-4 right-4 bg-red-500 text-white px-2 py-1 text-xs shadow-lg">
        Fixed Box
      </div>
    </div>

    <!-- Sticky -->
    <div class="bg-gray-200 p-4 border h-[200px] overflow-auto">
      <p class="text-sm font-semibold">Sticky (header menempel saat scroll) awalnya normal, lalu menempel ke atas saat scroll.</p>
      <div class="h-[300px]">
        <div class="sticky top-0 bg-yellow-400 text-white px-2 py-1">Sticky Header</div>
        <p class="mt-24">Scroll me...</p>
      </div>
    </div>
  </div>

  
</template>