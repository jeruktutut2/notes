# RESUMEABLE DOWNLOAD

## library
    go get github.com/labstack/echo/v4

## note
    mau tanya, prosesnya kan file di open dulu
    file, err := os.Open(filePath)
    baru kemudian di seek
    _, err = file.Seek(startByte, io.SeekStart)
    kemudian di kirim ke client untuk di download
    apakah memungkinkan file tidak diopen (diload ke memory) dulu tapi langsung di seek, agar yang diload ke memory hanya yang di seek

    🔍 Pertanyaan Utama:
    Apakah memungkinkan untuk melakukan Seek tanpa benar-benar membuka seluruh file ke memory, agar yang dibaca cuma bagian dari byte yang dibutuhkan?

    ✅ Jawabannya: Iya!
    Di Go, ketika kamu melakukan:

    file, err := os.Open(filePath)
    ➡️ Ini tidak berarti seluruh isi file di-load ke memory.

    os.Open hanya membuka file sebagai handle/stream, bukan membaca semua isinya ke dalam RAM.

    Jadi kamu aman — tidak boros memory walaupun file besar.

    🧠 Penjelasan Detail:
    os.Open() hanya membuka file dan mengembalikan *os.File, yaitu file descriptor yang siap dipakai untuk baca/seek.

    file.Seek(startByte, io.SeekStart) hanya menggeser posisi pembacaan pointer file.

    Saat kamu io.CopyN(c.Response().Writer, file, length), barulah Go mulai membaca byte demi byte dari posisi startByte, dan langsung streaming ke client — tidak di-buffer penuh ke memory.

    📦 Contoh Lengkap (resumable download handler)

    file, err := os.Open(filePath) // tidak load seluruh file
    if err != nil {
        return err
    }
    defer file.Close()

    file.Seek(startByte, io.SeekStart) // loncat ke posisi byte

    io.CopyN(c.Response().Writer, file, length) // stream byte langsung ke response
    🚀 Jadi Kesimpulannya:

    Proses	Di-load ke memory penuh?	Penjelasan
    os.Open()	❌ Tidak	Cuma buka file descriptor
    Seek(...)	❌ Tidak	Geser posisi pembacaan file
    CopyN(...)	❌ Tidak	Baca byte per byte, langsung stream ke client
    Kalau kamu ingin optimalkan lebih lanjut, kamu bisa kombinasikan dengan:

    Buffer size kecil (misal pakai bufio.Reader)

    Limit bandwidth (kalau perlu throttle)

    Kalau kamu tertarik ke efisiensi resource atau bandingkan dengan memory-mapped file (mmap), bisa juga kita bahas!

    🧵 Pendekatan 2: Memory Mapping (Opsional/Advanced)
    Kalau kamu benar-benar butuh akses cepat ke bagian tertentu dalam file (misalnya aplikasi audio/video editing), kamu bisa pakai memory-mapped file seperti dengan package golang.org/x/exp/mmap (external).

    Tapi ini jarang diperlukan untuk kebutuhan resumable download sederhana.

    📌 Contoh (Opsional):
    import "golang.org/x/exp/mmap"

    reader, err := mmap.Open(filePath)
    defer reader.Close()

    buf := make([]byte, length)
    _, err = reader.ReadAt(buf, startByte)

    c.Response().Writer.Write(buf)

    ✅ Kelebihan:
    Akses byte-range sangat cepat (langsung dari OS memory).

    Efisien untuk file akses acak sangat besar.

    ❌ Kekurangan:
    Tidak native di Go, harus pakai library eksternal.

    Tidak bisa pakai Seek seperti *os.File.

    Belum tentu lebih cepat kalau cuma mau streaming file ke client.

    ✨ Kesimpulan:

    Pendekatan	Cocok untuk	Efisien?	Support streaming?
    os.Open + Seek + CopyN	Semua file lokal, download biasa	✅	✅
    mmap (memory-mapped)	Akses acak byte untuk file besar	⚠️ (tergantung kasus)	❌ Tidak langsung



    tolong bahas yang 
    Buffer size kecil (misal pakai bufio.Reader)
    dan
    Limit bandwidth (kalau perlu throttle)

    🧵 1. Buffer Size Kecil (Gunakan bufio.Reader)
    🎯 Tujuan:
    Mengontrol jumlah data yang dibaca sekaligus dari file.

    Bisa lebih hemat memory (terutama kalau kamu ingin mengatur ukuran per part).

    Cocok kalau kamu ingin menggabungkan logika sendiri, misalnya untuk progress atau validasi manual.

    📌 Contoh Kode dengan bufio.Reader:
    file, err := os.Open(filePath)
    if err != nil {
        return err
    }
    defer file.Close()

    // Loncat ke posisi awal
    _, err = file.Seek(startByte, io.SeekStart)
    if err != nil {
        return err
    }

    // Buat reader dengan buffer
    reader := bufio.NewReaderSize(file, 4096) // 4KB buffer

    buffer := make([]byte, 4096)
    var sent int64 = 0

    for sent < length {
        toRead := int64(len(buffer))
        if length-sent < toRead {
            toRead = length - sent
        }

        n, err := reader.Read(buffer[:toRead])
        if n > 0 {
            c.Response().Write(buffer[:n])
            sent += int64(n)
        }

        if err != nil {
            if err == io.EOF {
                break
            }
            return err
        }
    }
    ✅ Keuntungan:
    Bisa mengontrol ukuran baca per iterasi.

    Bisa sisipkan fitur tambahan seperti progress atau logging per blok.

    🧵 2. Throttle / Limit Bandwidth
    🎯 Tujuan:
    Membatasi kecepatan download (misalnya 100 KB/s).

    Berguna untuk reseller, multi-user, atau admin control.

    📌 Contoh Kode dengan Delay (time.Sleep) untuk Throttle:
    const (
        bufferSize  = 4096             // 4KB
        throttleRate = 100 * 1024      // 100KB/s
        delayPerChunk = time.Second * bufferSize / throttleRate
    )

    buffer := make([]byte, bufferSize)
    reader := bufio.NewReaderSize(file, bufferSize)

    for {
        n, err := reader.Read(buffer)
        if n > 0 {
            c.Response().Write(buffer[:n])
            c.Response().Flush() // penting supaya data langsung dikirim

            time.Sleep(delayPerChunk) // throttle
        }

        if err != nil {
            if err == io.EOF {
                break
            }
            return err
        }
    }
    ✅ Keuntungan:
    Bisa limit kecepatan download per user.

    Bisa digunakan untuk menghindari overload server atau mengatur quota.

    ❌ Kekurangan:
    Sifatnya sederhana, tidak presisi, tapi cukup efektif.

    Kalau perlu presisi tinggi, kamu bisa pakai third-party package seperti github.com/juju/ratelimit.

    🔧 Bonus: Gunakan Flush pada c.Response() di Echo
    Supaya data dikirim langsung (streaming), tambahkan:

    c.Response().Flush()
    Ini penting kalau kamu ingin user lihat progress download secara real-time.

    🔚 Kesimpulan

    Teknik	Tujuan	Gunakan Saat
    bufio.Reader dengan buffer kecil	Kontrol memori dan kecepatan baca file	Mau progresif, hemat memory
    time.Sleep throttling	Batasi kecepatan download	Server shared, atau ingin user A dan B adil
    Flush	Kirim data langsung	Ingin efek real-time streaming


    🧩 Struktur Fungsi: StreamWithThrottle
    🎯 Fungsionalitas:
    Baca file dari byte tertentu (startByte)

    Batasi panjang yang dikirim (length)

    Throttle: kirim data dengan delay per chunk

    Gunakan bufio.Reader agar hemat memori

    📦 File: utils/file_stream.go
    package utils

    import (
	    "bufio"
	    "io"
	    "net/http"
	    "os"
	    "time"
    )

    type StreamConfig struct {
	    FilePath     string
	    StartByte    int64
	    Length       int64
	    Writer       http.ResponseWriter
	    BufferSize   int
	    BytesPerSec  int64 // Misalnya 100*1024 untuk 100KB/s
	    ContentType  string
    }

    func StreamWithThrottle(cfg StreamConfig) error {
	    file, err := os.Open(cfg.FilePath)
	    if err != nil {
		    return err
	    }
	    defer file.Close()

	    // Seek ke posisi mulai
	    _, err = file.Seek(cfg.StartByte, io.SeekStart)
	    if err != nil {
		    return err
	    }

	    // Set header kalau belum
	    if cfg.ContentType != "" {
		    cfg.Writer.Header().Set("Content-Type", cfg.ContentType)
	    }
	    cfg.Writer.WriteHeader(http.StatusPartialContent)

	    // Hitung delay per chunk
	    if cfg.BufferSize == 0 {
		    cfg.BufferSize = 4096 // default 4KB
	    }
	    if cfg.BytesPerSec == 0 {
		    cfg.BytesPerSec = 100 * 1024 // default 100KB/s
	    }
	    delayPerChunk := time.Second * time.Duration(cfg.BufferSize) / time.Duration(cfg.BytesPerSec)

	    reader := bufio.NewReaderSize(file, cfg.BufferSize)
	    buffer := make([]byte, cfg.BufferSize)
	    var sent int64 = 0

	    for sent < cfg.Length {
		    toRead := int64(len(buffer))
		    if cfg.Length-sent < toRead {
			    toRead = cfg.Length - sent
		    }

		    n, err := reader.Read(buffer[:toRead])
		    if n > 0 {
			    _, writeErr := cfg.Writer.Write(buffer[:n])
			    if writeErr != nil {
				    return writeErr // client closed?
			    }
			    sent += int64(n)

			    if f, ok := cfg.Writer.(http.Flusher); ok {
				    f.Flush()
			    }

			    time.Sleep(delayPerChunk)
		    }

		    if err != nil {
			    if err == io.EOF {
				    break
			    }
			    return err
		    }
	    }

	    return nil
    }

    ✅ Cara Pakai di Controller Echo:
    import "your_project/utils"

    func DownloadPartHandler(c echo.Context) error {
	    startByte := ... // parse dari range header
	    endByte := ...
	    length := endByte - startByte + 1

	    err := utils.StreamWithThrottle(utils.StreamConfig{
		    FilePath:    "path/to/your/file.mp4",
		    StartByte:   startByte,
		    Length:      length,
		    Writer:      c.Response(),
		    BufferSize:  4096,
		    BytesPerSec: 100 * 1024,
		    ContentType: "video/mp4",
	    })
	    if err != nil {
		    return c.JSON(http.StatusInternalServerError, echo.Map{
			    "error": err.Error(),
		    })
	    }
	    return nil
    }

    🚀 Tambahan Opsional:
    Kamu bisa tambahkan logika seperti progressCallback di config kalau ingin update UI.

    Bisa juga digunakan untuk video streaming, file zip besar, dll.

    Siap! Versi context.Context akan sangat berguna untuk:

    Menghentikan proses download saat client disconnect

    Graceful shutdown aplikasi

    ✅ Update: StreamWithThrottleContext()
    Kita buat versi yang menerima ctx context.Context, dan selama membaca atau menulis file, akan cek apakah context sudah dibatalkan.

    📦 File: utils/file_stream.go
    package utils

    import (
	    "bufio"
	    "context"
	    "io"
	    "net/http"
	    "os"
	    "time"
    )

    type StreamConfig struct {
	    Ctx          context.Context
	    FilePath     string
	    StartByte    int64
	    Length       int64
	    Writer       http.ResponseWriter
	    BufferSize   int
	    BytesPerSec  int64
	    ContentType  string
    }

    func StreamWithThrottleContext(cfg StreamConfig) error {
	    file, err := os.Open(cfg.FilePath)
	    if err != nil {
		    return err
	    }
	    defer file.Close()

	    _, err = file.Seek(cfg.StartByte, io.SeekStart)
	    if err != nil {
		    return err
	    }

	    if cfg.ContentType != "" {
		    cfg.Writer.Header().Set("Content-Type", cfg.ContentType)
	    }
	    cfg.Writer.WriteHeader(http.StatusPartialContent)

	    if cfg.BufferSize == 0 {
		    cfg.BufferSize = 4096
	    }
	    if cfg.BytesPerSec == 0 {
		    cfg.BytesPerSec = 100 * 1024
	    }
	    delayPerChunk := time.Second * time.Duration(cfg.BufferSize) / time.Duration(cfg.BytesPerSec)

	    reader := bufio.NewReaderSize(file, cfg.BufferSize)
	    buffer := make([]byte, cfg.BufferSize)
	    var sent int64 = 0

	    for sent < cfg.Length {
		    select {
		    case <-cfg.Ctx.Done():
			    return cfg.Ctx.Err() // context cancelled or timeout
		    default:
			    toRead := int64(len(buffer))
			    if cfg.Length-sent < toRead {
				    toRead = cfg.Length - sent
			    }

			    n, err := reader.Read(buffer[:toRead])
			    if n > 0 {
				    _, writeErr := cfg.Writer.Write(buffer[:n])
				    if writeErr != nil {
					    return writeErr
				    }
				    sent += int64(n)

				    if f, ok := cfg.Writer.(http.Flusher); ok {
					    f.Flush()
				    }
				    time.Sleep(delayPerChunk)
			    }

			    if err != nil {
				    if err == io.EOF {
					    break
				    }
				    return err
			    }
		    }
	    }

	    return nil
    }

    ✅ Cara Pakai di Echo Controller:

    import (
	    "your_project/utils"
    )

    func DownloadWithContextHandler(c echo.Context) error {
	    startByte := ... // parse range
	    endByte := ...
	    length := endByte - startByte + 1

	    err := utils.StreamWithThrottleContext(utils.StreamConfig{
		    Ctx:         c.Request().Context(), // penting!
		    FilePath:    "path/to/video.mp4",
		    StartByte:   startByte,
		    Length:      length,
		    Writer:      c.Response(),
		    BufferSize:  4096,
		    BytesPerSec: 100 * 1024,
		    ContentType: "video/mp4",
	    })
	    if err != nil {
		    if err == context.Canceled {
			    // Client disconnected
			    return nil
		    }
		    return c.JSON(http.StatusInternalServerError, echo.Map{
			    "error": err.Error(),
		    })
	    }
	    return nil
    }

    🧠 Bonus Pengetahuan:
    Echo akan otomatis membatalkan c.Request().Context() jika:

    User menutup browser/tab

    Timeout dari middleware seperti middleware.Timeout()

    Server shutdown