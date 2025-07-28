<script>
    const log = async () => {
        console.log("console log from remote svelte")
    }
</script>

<main>
    <div>
        <button class="bg-green-500 text-white px-4 py-2 rounded" on:click={log}>Log</button>
    </div>
</main>