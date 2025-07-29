<script>
    const partSize = 1024 * 1024
    let progress = 0

    const getFileStat = async () => {
        const response = await fetch("/file/stat", {
            method: 'GET',
        })
        const responseJson = await response.json()
        // const fileSize = responseJson.size
        return responseJson.size
    }

    const downloadByRange = async (start, end) => {
        return await fetch("/file/download", {
            method: 'GET',
            headers: {
                "Range": `bytes=${start}-${end}`
            }
        })
    }

    const download = async () => {
        console.log("start download")
        const parts = []
        try {
            const fileSize = await getFileStat()
            if (!fileSize) {
                console.log("cannot get filesize")
                // downloading.value = false
                return
            }
            const totalParts = Math.ceil(fileSize/partSize)
            for (let i = 0; i < totalParts; i++) {
                const start = i * partSize
                const end = Math.min(start + partSize - 1, fileSize - 1)
                const response = await downloadByRange(start, end)
                const buffer = new Uint8Array(await response.arrayBuffer())
                parts.push(buffer)
                // progress.value = Math.round(((i + 1) / totalParts) * 100)
            }

            const finalBlob = new Blob(parts)
            const blobUrl = URL.createObjectURL(finalBlob)

            const link = document.createElement("a")
            link.href = blobUrl
            link.download = "file_upload.mp4"
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
            // downloading.value = false
            console.log("successfully download")
        } catch(e) {
            console.log("error: ", e)
        }
    }

    let pause = false
    let currentStart = 0
    let chunks = []
    const startDownload = async () => {
        console.log("start download")
        const fileSize = await getFileStat()
        try {
            while (currentStart < fileSize) {
                if (pause) {
                    console.log("pause")
                    return
                }
                const end = Math.min(currentStart + partSize - 1, fileSize - 1)
                const response = await downloadByRange(currentStart, end)
                const buffer = new Uint8Array(await response.arrayBuffer())
                chunks.push(buffer)
                currentStart += partSize
            }
            const finalBlob = new Blob(chunks)
            const blobUrl = URL.createObjectURL(finalBlob)

            const link = document.createElement("a")
            link.href = blobUrl
            link.download = "file_upload.mp4"
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
            console.log("successfully download")
        } catch(e) {
            console.log("error: ", e)
        }
    }
    const pauseDownload = async () => {
        pause = true
    }
    const resumeDownload = async () => {
        pause = false
        startDownload()
    }

</script>
<!-- <h1>Welcome to SvelteKit</h1> -->
<!-- <p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p> -->

<div class="p-4 max-w-lg mx-auto">
    <h2 class="text-xl font-semibold mb-2">Resumable Download Demo</h2>
    <div>
        <button on:click={download} class="bg-blue-500 text-white px-4 py-2 rounded">Download</button>
    </div>

    <div>
        <button on:click={startDownload} class="bg-blue-500 text-white px-4 py-2 rounded">Start Download</button>
        <button on:click={pauseDownload} class="bg-blue-500 text-white px-4 py-2 rounded">Pause Download</button>
        <button on:click={resumeDownload} class="bg-blue-500 text-white px-4 py-2 rounded">Resume Download</button>
    </div>
</div>