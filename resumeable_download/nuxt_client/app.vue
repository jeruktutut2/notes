<script setup>
    import { ref } from 'vue'
    
    const partSize = 1024 * 1024
    const progress = ref(0)
    const downloading = ref(false)

    const getFileStat = async () => {
        const response = await fetch("/file/stat", {
            method: 'GET',
        })
        const responseJson = await response.json()
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
        const parts = []
        try {
            downloading.value = true
            const fileSize = await getFileStat()
            if (!fileSize) {
                console.log("cannot get filesize")
                downloading.value = false
                return
            }

            const totalParts = Math.ceil(fileSize/partSize)
            for (let i = 0; i < totalParts; i++) {
                const start = i * partSize
                const end = Math.min(start + partSize - 1, fileSize - 1)
                const response = await downloadByRange(start, end)
                const buffer = new Uint8Array(await response.arrayBuffer())
                parts.push(buffer)
                progress.value = Math.round(((i + 1) / totalParts) * 100)
            }

            const finalBlob = new Blob(parts)
            const blobUrl = URL.createObjectURL(finalBlob)

            const link = document.createElement("a")
            link.href = blobUrl
            link.download = "file_upload.mp4"
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
            downloading.value = false
        } catch(e) {
            console.log("error: ", e)
        }
    }

    const pause = ref(false)
    let currentStart = 0
    let chunks = []
    const startDownload = async () => {
        console.log("start download")
        const fileSize = await getFileStat()
        try {
            while (currentStart < fileSize) {
                if (pause.value) {
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
        pause.value = true
    }
    const resumeDownload = async () => {
        pause.value = false
        startDownload()
    }
</script>

<template>
    <div class="p-4 max-w-lg mx-auto">
        <h2 class="text-xl font-semibold mb-2">Resumable Download Demo</h2>
        <div>
            <button @click="download" class="bg-blue-500 text-white px-4 py-2 rounded" :disabled="downloading">
                {{ downloading ? 'Downloading...' : 'Download File' }}
            </button>
        </div>

        <div class="mt-4" v-if="downloading">
            <div class="w-full bg-gray-200 h-4 rounded">
              <div class="h-4 bg-green-500 rounded" :style="{ width: progress + '%' }"></div>
            </div>
            <p class="mt-1 text-sm">{{ progress }}%</p>
        </div>

        <div>
            <button @click="startDownload" class="bg-blue-500 text-white px-4 py-2 rounded">Start Download</button>
            <button @click="pauseDownload" class="bg-blue-500 text-white px-4 py-2 rounded">Pause Download</button>
            <button @click="resumeDownload" class="bg-blue-500 text-white px-4 py-2 rounded">Resume Download</button>
        </div>
    </div>
</template>
