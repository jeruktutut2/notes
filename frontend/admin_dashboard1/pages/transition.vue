<template>
    <div class="space-y-6 p-6 bg-gray-100 min-h-screen">

<!-- Transition All -->
<button class="bg-blue-500 text-white px-4 py-2 transition-all duration-300 hover:bg-blue-700">
  transition-all
</button>

<!-- Transition Colors -->
<button class="bg-green-500 text-white px-4 py-2 transition-colors duration-300 hover:bg-green-700">
  transition-colors
</button>

<!-- Transition Opacity -->
<button class="bg-red-500 text-white px-4 py-2 transition-opacity duration-300 hover:opacity-50">
  transition-opacity
</button>

<!-- Transition Transform -->
<button class="bg-purple-500 text-white px-4 py-2 transform transition-transform duration-300 hover:scale-110">
  transition-transform + scale
</button>

<!-- Transition Shadow -->
<button class="bg-yellow-500 text-white px-4 py-2 transition-shadow duration-300 hover:shadow-xl">
  transition-shadow
</button>

<!-- Duration and Easing -->
<button class="bg-gray-800 text-white px-4 py-2 transition-all duration-700 ease-in-out hover:bg-gray-600">
  duration + ease
</button>

</div>

</template>