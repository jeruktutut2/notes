<script>
    let requestId = ""
    let loading = false

    async function getRequestId() {
        // console.log("mantap")
        loading = true
        try {
            const response = await fetch("/request-id")
            const json = await response.json()
            requestId = json?.data?.requestId || "failed get request id"
        } catch(e) {
            loading = false
            requestId = "an error has accured"
            console.log("error:", e)
        }
        loading = false
    }

    async function mantap() {
        console.log("mantap")
    }
</script>
<!-- <h1>Welcome to SvelteKit</h1> -->
<!-- <p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p> -->
<div class="flex flex-col items-center justify-center min-h-screen ">
    <p class="text-gray-700 text-lg font-medium py-2">{requestId || 'No request id'}</p>
    <button class="bg-blue-500 py-2 px-2 text-white rounded hover:bg-blue-600 transition" on:click={getRequestId}>{loading ? "loading..." : "GET REQUEST ID s"}</button>
</div>
