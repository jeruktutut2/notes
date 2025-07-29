<script>
    let file = null
    let chunkSize = 1024 * 1024
    let fileId = "file_upload"
    let indices = []
    let pause = false

    const handleFileChanged = (e) => {
        file = e.target.files[0]
    }

    const fullUpload = async () => {
        if (!file) return
        const totalChunks = Math.ceil(file.size / chunkSize)

        for (let i = 0; i < totalChunks; i++) {
            const start = i * chunkSize
            const end = Math.min(file.size, start + chunkSize)
            const chunk = file.slice(start, end)

            try{
                await fetch("/file/upload", {
                    method: 'POST',
                    headers: {
                        "X-File-Id": fileId,
                        "X-Chunk-Index": i
                    },
                    body: chunk
                })
            } catch(e) {
                console.log("error:", e)
            }
        }

        await fetch("/file/merge", {
            method: 'POST',
            headers: {
                "X-File-Id": fileId,
                "X-Total-Chunks": totalChunks
            }
        })

        console.log("sucess")
    }

    const firstUpload = async () => {
        if (!file) return
        
        const totalChunks = Math.ceil(file.size / chunkSize)

        for (let i = 0; i < totalChunks; i += 2) {
            const start = i * chunkSize
            const end = Math.min(file.size, start + chunkSize)
            const chunk = file.slice(start, end)

            try{
                await fetch("/file/upload", {
                    method: 'POST',
                    headers: {
                        "X-File-Id": fileId,
                        "X-Chunk-Index": i
                    },
                    body: chunk
                })
            } catch(e) {
                console.log("error:", e)
            }
        }

        console.log("first upload sucess")
    }

    const finalUpload = async () => {
        try {
            let response = await fetch(`/file/check-file/${fileId}`, {
                method: 'GET'
            })
            let responseJson = await response.json()
            indices.value = responseJson.response

            if (!file) return
            const totalChunks = Math.ceil(file.size / chunkSize)
            for (let i = 0; i < totalChunks; i++) {
                if (!indices.value.includes(i)) {
                    const start = i * chunkSize
                    const end = Math.min(file.size, start + chunkSize)
                    const chunk = file.slice(start, end)

                    try{
                        await fetch("/file/upload", {
                            method: 'POST',
                            headers: {
                                "X-File-Id": fileId,
                                "X-Chunk-Index": i
                            },
                            body: chunk
                        })
                    } catch(e) {
                        console.log("error:", e)
                    }

                }
            }

            await fetch("/file/merge", {
                method: 'POST',
                headers: {
                    "X-File-Id": fileId,
                    "X-Total-Chunks": totalChunks
                }
            })

            console.log("final upload sucess")
        } catch(e) {
            console.log("error:", e)
        }
    }

    const initUpload = async () => {
        console.log("init upload")
        if (!file) return

        const totalChunks = Math.ceil(file.size / chunkSize)

        for (let i = 0; i < totalChunks; i++) {
            if (pause) {
                console.log("upload paused")
                return
            }
            const start = i * chunkSize
            const end = Math.min(file.size, start + chunkSize)
            const chunk = file.slice(start, end)

            const formData = new FormData()
            formData.append("chunk", chunk)

            try{
                await fetch("/file/upload", {
                    method: 'POST',
                    headers: {
                        "X-File-Id": fileId,
                        "X-Chunk-Index": i
                    },
                    body: chunk
                })
            } catch(e) {
                console.log("error:", e)
            }
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
        console.log("init success")
    }

    const pauseUpload = async () => {
        pause = true
        console.log("pause successfully")
    }

    const resumeUpload = async () => {
        pause = false

        try {
            let response = await fetch(`/file/check-file/${fileId}`, {
                method: 'GET'
            })
            let responseJson = await response.json()
            indices = responseJson.response

            if (!file) return

            const totalChunks = Math.ceil(file.size / chunkSize)
            for (let i = 0; i < totalChunks; i++) {
                if (!indices.includes(i)) {
                    const start = i * chunkSize
                    const end = Math.min(file.size, start + chunkSize)
                    const chunk = file.slice(start, end)

                    try{
                        await fetch("/file/upload", {
                            method: 'POST',
                            headers: {
                                "X-File-Id": fileId,
                                "X-Chunk-Index": i
                            },
                            body: chunk
                        })
                    } catch(e) {
                        console.log("error:", e)
                    }
                }
            }

            await fetch("/file/merge", {
                method: 'POST',
                headers: {
                    "X-File-Id": fileId,
                    "X-Total-Chunks": totalChunks
                }
            })
            
            console.log("resume upload successfully")
        } catch(e) {
            console.log("error: ", e)
        }
    }

    const uploadAndMerge = async () => {
        console.log("start upload")
        if (!file) return

        const totalChunks = Math.ceil(file.size / chunkSize)

        for (let i = 0; i < totalChunks; i++) {
            const start = i * chunkSize
            const end = Math.min(file.size, start + chunkSize)
            const chunk = file.slice(start, end)

            try {
                let formData = new FormData()
                formData.append("fileId", fileId)
                formData.append("chunkIndex", i)
                formData.append("lastChunkIndex", totalChunks - 1)
                formData.append("chunk", chunk)

                let response = await fetch("/file/upload-merge", {
                    method: 'POST',
                    body: formData
                })
                console.log("response: ", await response.json())
            } catch(e) {
                console.log("error: ", e)
            }
        }
        console.log("success")
    }
    // if you want to add prevent action if someone refresh the page, you can save the last index part file upload and progress value to localstorage
</script>

<div>
    <input type="file" on:change={handleFileChanged} />
    <div>
        <button class="bg-blue-500 text-white px-4 py-2 mt-2" on:click={fullUpload}>Full Upload</button>
    </div>
    <div>
        <button class="bg-blue-500 text-white px-4 py-2 mt-2" on:click={firstUpload}>First Upload</button>
        <button class="bg-blue-500 text-white px-4 py-2 mt-2" on:click={finalUpload}>Final Upload</button>
    </div>
    <div>
        <button class="bg-blue-500 text-white px-4 py-2 mt-2" on:click={initUpload}>Init Upload</button>
        <button class="bg-blue-500 text-white px-4 py-2 mt-2" on:click={pauseUpload}>Pause Upload</button>
        <button class="bg-blue-500 text-white px-4 py-2 mt-2" on:click={resumeUpload}>Resume Upload</button>
    </div>
    <div>
        <button class="bg-blue-500 text-white px-4 py-2 mt-2" on:click={uploadAndMerge}>Upload and Merge</button>
    </div>
</div>