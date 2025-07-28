<template>
    <div class="bg-gray-100 min-h-screen">
        <div class="flex min-h-screen relative">

<!-- Sidebar -->
<aside id="sidebar"
  class="fixed lg:static z-40 bg-white w-64 h-full transition-transform duration-300 transform -translate-x-full lg:translate-x-0">
  <div class="p-4 border-b font-bold text-gray-900">My Dashboard</div>
  <nav class="p-4 space-y-2">
    <a href="#" class="block text-gray-700 hover:text-blue-600">Home</a>
    <a href="#" class="block text-gray-700 hover:text-blue-600">Reports</a>
    <a href="#" class="block text-gray-700 hover:text-blue-600">Settings</a>
  </nav>
</aside>

<!-- Overlay (mobile) -->
<div id="overlay"
  class="fixed inset-0 bg-black bg-opacity-30 z-30 hidden lg:hidden"
  onclick="toggleSidebar()"></div>

<!-- Main content -->
<div class="flex-1 flex flex-col">

  <!-- Header -->
  <header class="bg-white shadow p-4 flex items-center justify-between">
    <!-- Burger -->
    <button class="lg:hidden" onclick="toggleSidebar()">
      <!-- Bars Icon (Heroicon: Bars3) -->
      <svg class="w-6 h-6 text-gray-700" fill="none" stroke="currentColor" stroke-width="2"
        viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round"
          d="M4 6h16M4 12h16M4 18h16" />
      </svg>
    </button>
    <h1 class="text-lg font-semibold text-gray-800">Dashboard</h1>
  </header>

  <!-- Main content area -->
  <main class="p-6 flex-1">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
      <!-- Card -->
      <div class="bg-white p-4 rounded-lg shadow">
        <h2 class="text-lg font-semibold text-gray-900">Revenue</h2>
        <p class="text-2xl font-bold mt-2">$24,000</p>
        <p class="text-sm text-gray-500">Compared to last month</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <h2 class="text-lg font-semibold text-gray-900">Users</h2>
        <p class="text-2xl font-bold mt-2">1,230</p>
        <p class="text-sm text-gray-500">New signups</p>
      </div>
      <div class="bg-white p-4 rounded-lg shadow">
        <h2 class="text-lg font-semibold text-gray-900">Projects</h2>
        <p class="text-2xl font-bold mt-2">12</p>
        <p class="text-sm text-gray-500">Active this week</p>
      </div>
    </div>
  </main>

</div>
</div>
    </div>
</template>