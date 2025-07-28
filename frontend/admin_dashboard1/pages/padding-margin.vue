<script setup>
</script>
<template>
    <div class="space-y-6 p-4">

        <!-- Padding -->
        <div class="bg-blue-100 p-4">
            <div class="bg-blue-400 text-white">Padding 4 (p-4)</div>
        </div>

        <!-- Margin -->
        <div class="bg-green-100">
            <div class="bg-green-400 text-white m-4">Margin 4 (m-4)</div>
        </div>

        <!-- Padding + Margin -->
        <div class="bg-yellow-100">
            <div class="bg-yellow-400 text-white m-4 p-4">Margin 4 + Padding 4 (m-4 p-4)</div>
        </div>

    </div>

    <div class="min-h-screen bg-gray-100 p-6">
        <!-- Header -->
        <h1 class="text-2xl font-bold mb-6">Dashboard</h1>

        <!-- Grid Card -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- Card 1 -->
            <div class="bg-white rounded shadow p-4">
                <h2 class="text-lg font-semibold mb-2">Users</h2>
                <p class="text-3xl font-bold text-blue-600">1,234</p>
            </div>

            <!-- Card 2 -->
            <div class="bg-white rounded shadow p-4">
                <h2 class="text-lg font-semibold mb-2">Revenue</h2>
                <p class="text-3xl font-bold text-green-600">$12,345</p>
            </div>

            <!-- Card 3 -->
            <div class="bg-white rounded shadow p-4">
                <h2 class="text-lg font-semibold mb-2">Orders</h2>
                <p class="text-3xl font-bold text-yellow-600">567</p>
            </div>
        </div>
  </div>
</template>