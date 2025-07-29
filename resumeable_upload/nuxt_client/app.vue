<script setup>
    import { ref } from 'vue'
    const file = ref(null);
    const pause = ref(false)
    const chunkSize = 1024 * 1024 // 1MB
    const fileId = "file_upload"
    const indices = ref([])

    const handleFileChanged = (e) => {
        file.value = e.target.files[0]
    }

    const fullUpload = async () => {
        if (!file) return
        const totalChunks = Math.ceil(file.value.size / chunkSize)

        for (let i = 0; i < totalChunks; i++) {
            const start = i * chunkSize
            const end = Math.min(file.value.size, start + chunkSize)
            const chunk = file.value.slice(start, end)

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
        
        const totalChunks = Math.ceil(file.value.size / chunkSize)

        for (let i = 0; i < totalChunks; i += 2) {
            const start = i * chunkSize
            const end = Math.min(file.value.size, start + chunkSize)
            const chunk = file.value.slice(start, end)

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
            const totalChunks = Math.ceil(file.value.size / chunkSize)
            for (let i = 0; i < totalChunks; i++) {
                if (!indices.value.includes(i)) {
                    const start = i * chunkSize
                    const end = Math.min(file.value.size, start + chunkSize)
                    const chunk = file.value.slice(start, end)

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

        const totalChunks = Math.ceil(file.value.size / chunkSize)

        for (let i = 0; i < totalChunks; i++) {
            if (pause.value) {
                console.log("upload paused")
                return
            }
            const start = i * chunkSize
            const end = Math.min(file.value.size, start + chunkSize)
            const chunk = file.value.slice(start, end)

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
        pause.value = true
        console.log("pause successfully")
    }

    const resumeUpload = async () => {
        pause.value = false

        try {
            let response = await fetch(`/file/check-file/${fileId}`, {
                method: 'GET'
            })
            let responseJson = await response.json()
            indices.value = responseJson.response

            if (!file) return

            const totalChunks = Math.ceil(file.value.size / chunkSize)
            for (let i = 0; i < totalChunks; i++) {
                if (!indices.value.includes(i)) {
                    const start = i * chunkSize
                    const end = Math.min(file.value.size, start + chunkSize)
                    const chunk = file.value.slice(start, end)

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

        const totalChunks = Math.ceil(file.value.size / chunkSize)

        for (let i = 0; i < totalChunks; i++) {
            const start = i * chunkSize
            const end = Math.min(file.value.size, start + chunkSize)
            const chunk = file.value.slice(start, end)

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
<template>
    <div>
        <input type="file" @change="handleFileChanged" />
        <div>
            <button @click="fullUpload">Full Upload</button>
        </div>
        <div>
            <button @click="firstUpload">First Upload</button>
            <button @click="finalUpload">Final Upload</button>
        </div>
        <div>
            <button @click="initUpload">Init Upload</button>
            <button @click="pauseUpload">Pause Upload</button>
            <button @click="resumeUpload">Resume Upload</button>
        </div>
        <div>
            <button @click="uploadAndMerge">Upload and Merge</button>
        </div>
    </div>
</template>
