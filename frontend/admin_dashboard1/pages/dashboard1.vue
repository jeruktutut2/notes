<template>
    <section class="bg-gray-100 min-h-screen p-6">
  <!-- Header -->
  <header class="mb-6">
    <h1 class="text-2xl font-bold text-gray-900">Dashboard Overview</h1>
    <p class="text-sm text-gray-600">Summary of your activity this month</p>
  </header>

  <!-- Row Cards -->
  <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
    <!-- Card 1 -->
    <div class="bg-white p-4 rounded-lg shadow hover:shadow-md transition">
      <div class="flex items-center justify-between">
        <h2 class="text-lg font-semibold text-gray-900">Revenue</h2>
        <svg class="w-5 h-5 text-gray-400 hover:text-gray-600 cursor-pointer" fill="none" stroke="currentColor" stroke-width="2"
          viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01"></path>
        </svg>
      </div>
      <p class="text-2xl font-bold text-gray-900 mt-2">$24,000</p>
      <p class="text-sm text-gray-500">Compared to last month</p>
    </div>

    <!-- Card 2 -->
    <div class="bg-white p-4 rounded-lg shadow hover:shadow-md transition">
      <h2 class="text-lg font-semibold text-gray-900">New Users</h2>
      <p class="text-2xl font-bold text-gray-900 mt-2">1,230</p>
      <p class="text-sm text-gray-500">In the last 30 days</p>
    </div>

    <!-- Card 3 -->
    <div class="bg-white p-4 rounded-lg shadow hover:shadow-md transition">
      <h2 class="text-lg font-semibold text-gray-900">Active Projects</h2>
      <p class="text-2xl font-bold text-gray-900 mt-2">12</p>
      <p class="text-sm text-gray-500">Currently ongoing</p>
    </div>
  </div>

  <!-- Divider -->
  <hr class="my-8 border-gray-300" />

  <!-- Call to Action -->
  <div class="flex justify-between items-center bg-white p-4 rounded-lg shadow">
    <p class="text-gray-800">Need more detailed reports?</p>
    <button
      class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition font-medium">
      View Full Reports
    </button>
  </div>
</section>

</template>