'use client'

import Image from "next/image";

export default function Home() {
    const partSize = 1024 * 1024

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
        console.log("download")
        const parts = []
        try {
            const fileSize = await getFileStat()
            if (!fileSize) {
                console.log("cannot get filesize")
                return
            }

            const totalParts = Math.ceil(fileSize/partSize)
            for (let i = 0; i < totalParts; i++) {
                const start = i * partSize
                const end = Math.min(start + partSize - 1, fileSize - 1)
                const response = await downloadByRange(start, end)
                const buffer = new Uint8Array(await response.arrayBuffer())
                parts.push(buffer)
            }

            const finalBlob = new Blob(parts)
            const blobUrl = URL.createObjectURL(finalBlob)

            const link = document.createElement("a")
            link.href = blobUrl
            link.download = "file_upload.mp4"
            document.body.appendChild(link)
            link.click()
            document.body.removeChild(link)
            console.log("download successfully")
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

    return (
      <div className="p-4 max-w-lg mx-auto">
          <h2 className="text-xl font-semibold mb-2">Resumable Download Demo</h2>
          <div>
              <button onClick={download} className="bg-blue-500 text-white px-4 py-2 rounded">Download</button>
          </div>
          {/* <div class="mt-4" v-if="downloading">
              <div class="w-full bg-gray-200 h-4 rounded">
                  <div class="h-4 bg-green-500 rounded" :style="{ width: progress + '%' }"></div>
              </div>
              <p class="mt-1 text-sm">{{ progress }}%</p>
          </div> */}
          <div>
              <button onClick={startDownload} className="bg-blue-500 text-white px-4 py-2 rounded">Start Download</button>
              <button onClick={pauseDownload} className="bg-blue-500 text-white px-4 py-2 rounded">Pause Download</button>
              <button onClick={resumeDownload} className="bg-blue-500 text-white px-4 py-2 rounded">Resume Download</button>
          </div>
      </div>
    );
}
