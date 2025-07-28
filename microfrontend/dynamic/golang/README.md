# GATEWAY

## library
    go get github.com/labstack/echo/v4

## curl test
    curl -i -X GET http://localhost:8080/cookie/set-remote1
    curl -i -X GET http://localhost:8080/cookie/set-remote2
    curl -i -X GET -H "Cookie: remote=remote1;" http://localhost:8080/assets/remoteEntry.js
    curl -i -X GET -H "Cookie: remote=remote2;" http://localhost:8080/assets/remoteEntry.js
    curl -i -X GET -H "Cookie: remote=remote1;" http://localhost:8080/remote/remoteEntry.js
    curl -i -X GET -H "Cookie: remote=remote2;" http://localhost:8080/remote/remoteEntry.js
    curl -i -X GET -H "Cookie: remote=remote1;" http://localhost:8080/assets/remote
    curl -i -X GET -H "Cookie: remote=remote2;" http://localhost:8080/assets/remote

## note
    Masalah ini terjadi karena meskipun remoteEntry.js bisa dipanggil dari path /assets/remoteEntry.js melalui proxy, file-file internal/terusan (chunk seperti __federation_expose_Button-xxx.js) yang diminta oleh remoteEntry.js tidak otomatis melalui proxy, sehingga mereka gagal ditemukan atau muncul 404.
    🔍 Penjelasan Detail
    Saat kamu menggunakan:

    url: '/assets/remoteEntry.js',
    Browser memuat file ini dari:

    http://localhost:3000/assets/remoteEntry.js
    TAPI, isi remoteEntry.js (hasil build Vite remote) memuat import dinamis seperti:

    import('./__federation_expose_Button-xxx.js')
    Dan import itu relatif terhadap host (localhost:3000), bukan melalui proxy ke localhost:3001, jadi file itu tidak ditemukan.

    ✅ Solusi: Gunakan URL absolut dari remote
    Kembali gunakan URL penuh (hardcoded) seperti:

    url: 'http://localhost:3001/assets/remoteEntry.js'
    Kenapa?
    Karena ini akan memastikan semua dynamic import dari dalam remoteEntry.js juga berasal dari domain localhost:3001.

    ❗ Kenapa proxy tidak cukup?
    Vite hanya mem-proxy permintaan dari browser langsung ke server dev lokal, tapi:

    import dinamis di dalam remoteEntry.js tidak tahu bahwa kamu pakai proxy

    URL chunk yang dibuat Vite adalah relatif ke origin (dalam hal ini localhost:3000), sehingga import gagal jika remoteEntry.js berasal dari domain yang beda tapi tidak eksplisit.

    🛠 Opsi Lain (tidak disarankan):
    Jika kamu tetap ingin pakai proxy (misal /remote/remoteEntry.js), kamu harus juga proxy semua path assets/* ke localhost:3001, seperti:

server: {
  proxy: {
    '/remote': {
      target: 'http://localhost:3001',
      changeOrigin: true,
      rewrite: path => path.replace(/^\/remote/, '/assets'),
    },
    '/assets': {
      target: 'http://localhost:3001',
      changeOrigin: true,
    }
  }
}
    TAPI: ini bisa bentrok jika kamu juga punya assets sendiri dari Vite host.

    ✅ Rekomendasi Terbaik
    Selama development, gunakan URL absolut untuk remote:

    url: 'http://localhost:3001/assets/remoteEntry.js'
    Kalau ingin dinamis saat production, kamu bisa set berdasarkan env atau config.

    jika menggunakan base: /remote/ maka akses dari browser menjadi http://localhost:3001/remote/assets/remoteEntry.js

    SOLUSION
    persiapkan proxy pada frontend dan endpoint pada backend: /remote/remoteEntry.js dan /remote/* karena setelah fetch /remote/remoteEntry.js kemudian akan fetch lain-lainnya dan endpoint basenya adalah /remote
    tambahkan :key pada komponen remote yang ada di host, valuenya bebas yang penting berbeda antar komponen