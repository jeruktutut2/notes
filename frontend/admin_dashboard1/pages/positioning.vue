<script setup>
</script>
<template>
    <div class="p-6 space-y-8 bg-gray-100 min-h-screen">
    
        <!-- Static (default) -->
        <div class="bg-white border p-4">
            <p class="font-bold mb-2">Static (default) tidak bisa diposisikan dengan top/right dll.</p>
            <div class="static bg-gray-200 p-2">Box Static</div>
        </div>

        <!-- Relative -->
        <div class="bg-white border p-4">
            <p class="font-bold mb-2">Relative hanya membuat referensi untuk anak absolute.</p>
            <div class="relative bg-gray-200 p-2">Box Relative</div>
        </div>

        <!-- Absolute dalam parent relative -->
        <div class="bg-white border p-4 relative h-32">
            <p class="font-bold mb-2">Absolute (posisi dalam box relative) mengambang dalam parent yang relative.</p>
            <div class="absolute top-2 right-2 bg-blue-500 text-white text-sm px-2 py-1 rounded">
                ABSOLUTE
            </div>
            <div class="bg-gray-200 p-2 mt-8">Isi Box</div>
        </div>

        <!-- Fixed (selalu menempel layar) -->
        <div class="bg-white border p-4">
            <p class="font-bold mb-2">Fixed tetap di pojok layar walau scroll.</p>
            <p class="text-sm text-gray-600">Scroll ke bawah untuk melihat efeknya, ini untuk memperjelas efek box pojok kanan bawah</p>
        </div>

        <!-- Sticky -->
        <div class="bg-white border h-[300px] overflow-y-auto p-4">
            <p class="font-bold mb-2">Sticky (menempel saat scroll) awalnya normal, lalu menempel ke atas saat scroll.</p>
            <div class="h-[500px]">
                <div class="sticky top-0 bg-yellow-400 text-white px-2 py-1 shadow-md">
                    Sticky Header
                </div>
                <p class="mt-20">Scroll area ini untuk melihat efek sticky</p>
            </div>
        </div>

        <!-- Spacer to trigger scroll -->
        <div class="h-[400px]"></div>
  </div>

    <!-- Fixed Box -->
    <div class="fixed bottom-4 right-4 bg-red-500 text-white px-4 py-2 rounded shadow-lg">
        Fixed Box tetap di pojok layar walau scroll.
    </div>
</template>