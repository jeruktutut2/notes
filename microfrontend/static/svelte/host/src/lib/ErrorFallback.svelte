<script>
    export let errorMessage = "Failed to load component.";
</script>

<div class="flex flex-col items-center justify-center p-4 text-red-600 bg-red-100 rounded">
    <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 5.636l-12.728 12.728M5.636 5.636l12.728 12.728" />
    </svg>
    <h2 class="text-lg font-bold">Error</h2>
    <p class="text-sm mt-2 text-center">{errorMessage}</p>
  </div>