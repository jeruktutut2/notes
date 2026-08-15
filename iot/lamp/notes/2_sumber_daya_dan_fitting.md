# Sumber Daya Listrik dan Fitting Lampu Pintar

Dalam proyek IoT lampu pintar, terdapat tantangan perbedaan tegangan:
1.  **Lampu rumah** menggunakan tegangan tinggi **AC 220V**.
2.  **Mikrokontroler (ESP8266/ESP32)** bekerja pada tegangan rendah **DC 3.3V atau 5V**.

Berikut adalah penjelasan mengenai kebutuhan daya mikrokontroler dan solusi praktis untuk menyatukannya dengan fitting lampu.

---

## 1. Apakah Mikrokontroler Selalu Membutuhkan Charger HP?

Secara teknis, **ya**, mikrokontroler membutuhkan sumber daya DC yang stabil. 
Jika kita merakitnya secara terpisah (DIY dasar):
*   Lampu dihubungkan ke listrik AC 220V melalui relay.
*   ESP8266/ESP32 diberi daya terpisah menggunakan kabel micro-USB yang dicolokkan ke adaptor charger HP.

Namun, metode ini kurang praktis untuk dipasang di plafon karena memerlukan dua sumber colokan listrik terpisah (satu untuk lampu, satu untuk charger).

---

## 2. Solusi 1: Menggunakan Perangkat Jadi (Smart Fitting / Smart Adapter)
Jika Anda tidak ingin repot menyolder dan merakit adaptor daya, ada alat di pasaran yang menggabungkan fitting lampu, mikrokontroler, dan penurun tegangan (converter) menjadi satu alat:

### A. Fitting Pintar (E27 Smart Fitting Adapter)
*   **Contoh Produk**: **Sonoff Slampher R2** atau fitting pintar generik sejenisnya.
*   **Cara kerja**: Anda cukup memasang adapter ini ke fitting lampu plafon E27 yang sudah ada, lalu memasang lampu bohlam biasa di atasnya.
*   **Di dalamnya terdapat**:
    *   Sirkuit AC-to-DC internal yang mengambil daya dari 220V untuk menghidupkan chip mikrokontroler di dalamnya.
    *   Chip Wi-Fi (biasanya berbasis ESP8266/ESP8285).
    *   Relay internal untuk memutus dan menyambung arus ke lampu.
*   **Kelebihan**: Sangat aman, rapi, tinggal pakai, dan sudah tersertifikasi keselamatan.

### B. Produk Smart Home Komersial yang Menggunakan ESP32 Secara Langsung
Banyak produsen smart home kini bermigrasi dari ESP8266 ke **ESP32** (atau turunannya seperti ESP32-C3) karena memerlukan fitur Bluetooth untuk mempermudah proses *pairing* (koneksi awal ke HP) serta performa yang lebih stabil. Berikut beberapa contoh produk jadi yang menggunakan chip ESP32:

1.  **Shelly Plus Series (contoh: Shelly Plus 1, Shelly Plus 2PM)**:
    *   Ini adalah sakelar pintar berukuran sangat kecil yang ditanam di dalam mangkok sakelar dinding (*in-wall switch*).
    *   **Menggunakan ESP32**. Shelly sangat populer karena mereka sengaja menyediakan port khusus di casingnya agar pengguna bisa dengan mudah memprogram ulang (*flash*) chip ESP32 tersebut menggunakan firmware kustom seperti ESPHome atau Tasmota.
2.  **Sonoff MINIR4 (MINI Extreme)**:
    *   Sakelar pintar berukuran ultra-kecil untuk dipasang di belakang sakelar dinding rumah Anda.
    *   **Menggunakan ESP32** (peningkatan dari seri MINI sebelumnya yang masih memakai ESP8266). Fitur Bluetooth pada ESP32 di produk ini mempermudah pengguna saat menghubungkan perangkat pertama kali ke aplikasi eWeLink.
3.  **Sonoff NSPanel / NSPanel Pro**:
    *   Panel kontrol rumah pintar berlayar sentuh (*touchscreen*) yang dipasang di dinding.
    *   **Menggunakan ESP32** untuk mengelola layar sentuh, membaca sensor suhu internal, terhubung ke Wi-Fi, dan mengendalikan relay fisik lampu yang ada di belakangnya.
4.  **Athom Smart Plug & Smart Bulb**:
    *   Colokan pintar dan lampu pintar yang sudah di-flash dengan firmware *open-source* (ESPHome/Tasmota). Banyak varian terbaru mereka yang secara resmi menggunakan chip **ESP32-C3** (varian ESP32 berbasis RISC-V).

---

## 3. Solusi 2: Cara DIY (Merakit Sendiri di dalam Fitting)
Jika Anda tetap ingin merakit sendiri tetapi ingin dayanya menyatu (hanya menggunakan satu kabel AC 220V masuk), Anda membutuhkan komponen tambahan bernama **AC-to-DC Step Down Module**.

### Menggunakan Modul Hi-Link HLK-PM01 (atau HLK-PM03)
*   **Fungsi**: Mengubah arus listrik AC 220V langsung menjadi DC 5V (untuk HLK-PM01) atau DC 3.3V (untuk HLK-PM03) dengan ukuran yang sangat ringkas (sebesar kotak korek api).
*   **Cara Merakit**:
    1.  Listrik AC 220V dari PLN dimasukkan ke input **HLK-PM01** dan juga ke sakelar **Relay**.
    2.  Output DC 5V dari HLK-PM01 dihubungkan langsung ke pin `VIN` dan `GND` pada ESP8266/ESP32.
    3.  Mikrokontroler akan hidup secara otomatis dari listrik AC tersebut dan siap mengendalikan relay untuk menyalakan/mematikan lampu.
    4.  Seluruh komponen ini (ESP, Relay, HLK-PM01) dimasukkan ke dalam kotak proyek kecil (junction box) di dekat fitting lampu.

> [!WARNING]
> **Peringatan Keselamatan:** Merakit sendiri dengan arus AC 220V memiliki risiko sengatan listrik yang berbahaya. Pastikan sekring rumah (MCB) dimatikan saat melakukan pemasangan dan pastikan tidak ada kabel tembaga telanjang yang saling bersentuhan. Gunakan isolasi bakar (shrink tube) atau kotak casing plastik yang aman.

---

## 4. Status Program dan Dukungan MQTT pada Produk Komersial

Banyak pemula yang bingung apakah produk jadi di atas kosong (harus diprogram sendiri) atau siap pakai, serta bagaimana mereka terhubung ke jaringan seperti MQTT. Berikut penjelasannya:

### A. Apakah Produk Komersial Tersebut Sudah Diprogram?
**Ya, semua produk tersebut sudah diprogram oleh pabrik dan siap pakai.**
*   Saat dibeli, alat-alat ini memiliki aplikasi resmi masing-masing (Shelly menggunakan aplikasi Shelly Smart Control, Sonoff menggunakan eWeLink).
*   Anda tidak perlu menulis kode pemrograman apa pun. Cukup sambungkan kabel listrik AC, hubungkan ke Wi-Fi rumah lewat aplikasi di HP, dan alat langsung bekerja.

### B. Apakah Bisa Diprogram Ulang (Flash Ulang)?
**Ya, semuanya bisa.** Karena otaknya adalah chip ESP32 atau ESP8266, Anda bisa menghapus program bawaan pabrik dan memasukkan program buatan Anda sendiri (menggunakan C++, Rust, ESPHome, atau Tasmota).
*   **Shelly (Paling Mudah)**: Menyediakan port koneksi khusus (*header pin*) di luar casing, sehingga Anda bisa mencolokkan kabel pemrograman USB-to-UART tanpa perlu membongkar/merusak alat.
*   **Athom (Sudah Terbuka)**: Produk Athom memang sengaja dijual dengan firmware *open-source* (ESPHome/Tasmota) siap pakai di dalamnya.
*   **Sonoff (Perlu Dibongkar)**: Anda harus membuka casing plastiknya dan menyolder kabel kecil ke pin sirkuit internalnya agar bisa di-flash ulang.

### C. Apakah Semuanya Bisa Terhubung ke MQTT?
MQTT adalah protokol standar untuk komunikasi IoT lokal berkecepatan tinggi. Berikut status dukungan MQTT masing-masing alat **tanpa mengubah program bawaannya (firmware asli)**:

| Nama Produk | Mendukung MQTT Bawaan? | Keterangan |
| :--- | :--- | :--- |
| **Shelly Plus** | **YA** | Firmware asli Shelly mendukung MQTT secara *native*. Anda tinggal mengaktifkan fitur ini di halaman pengaturan perangkat. |
| **Athom** | **YA** | Karena sejak awal menggunakan Tasmota/ESPHome, alat ini sudah otomatis mendukung MQTT dengan sangat mudah. |
| **Sonoff (MINI / NSPanel)** | **TIDAK LANGSUNG** | Firmware bawaan Sonoff (eWeLink) terikat ke protokol cloud Sonoff sendiri. Agar bisa terkoneksi ke broker MQTT lokal Anda, Sonoff harus **diprogram ulang (di-flash)** dengan Tasmota atau ESPHome terlebih dahulu. |

---

## 5. Konsep Firmware vs Hardware: Mengapa Semua Bisa Diprogram Ulang?

Ada kesalahpahaman umum bahwa jika suatu alat sudah memiliki aplikasi bawaan (seperti Shelly Smart Control atau eWeLink), maka alat tersebut terkunci dan tidak bisa diprogram ulang. Mari kita pahami konsep dasarnya:

### A. Analogi Hardware vs Firmware
Bayangkan perangkat pintar komersial (Shelly, Sonoff, Athom) seperti sebuah **smartphone**:
*   **Hardware (Chip ESP32/ESP8266)**: Adalah fisik sirkuit elektronik dan memori flash di dalamnya (mirip fisik ponsel Anda).
*   **Firmware (Program/OS Bawaan)**: Adalah Sistem Operasi yang dipasang di dalamnya (seperti OS Android bawaan Samsung atau Xiaomi).
*   **Aplikasi Bawaan (eWeLink/Shelly App)**: Adalah aplikasi ekosistem yang terikat dengan Sistem Operasi bawaan tersebut.

Sama seperti ponsel Android yang bisa kita format ulang (*factory reset*) lalu di-install Sistem Operasi kustom lain (misalnya LineageOS), **chip ESP di dalam Sonoff, Shelly, dan Athom juga bisa diformat total.**

*   **Pilihan A (Gunakan Firmware Asli)**: Jika Anda tidak memprogram ulang chipnya, Anda menikmati kemudahan bawaan pabrik dengan aplikasi mereka (eWeLink / Shelly Smart Control).
*   **Pilihan B (Program Ulang / Flash Ulang)**: Jika Anda mengunggah program buatan sendiri (menggunakan C++/Arduino, Rust) atau OS open-source lain (Tasmota/ESPHome), **maka program asli bawaan pabrik akan terhapus bersih dari memori chip.** Alat tersebut kini 100% menjalankan kode baru Anda. Anda tidak bisa lagi memakai aplikasi eWeLink/Shelly, tetapi Anda bebas mengontrol alat tersebut sesuai keinginan Anda sendiri.

---

## 6. Mengenal Tasmota dan ESPHome

Bagi pehobi IoT, menulis kode C++ atau Rust dari nol untuk mengontrol relay, Wi-Fi, dan MQTT terkadang melelahkan. Oleh karena itu, komunitas pembuat open-source menciptakan **Tasmota** dan **ESPHome**.

*   **Apa itu?** Keduanya adalah Sistem Operasi (Firmware) siap pakai yang dirancang khusus untuk chip ESP8266/ESP32 agar perangkat bisa diintegrasikan ke sistem Smart Home lokal (tanpa cloud internet).
*   **Tasmota**: Setelah dipasang di ESP32, Tasmota menyediakan halaman konfigurasi berbasis web. Anda tinggal klik tombol di browser untuk menentukan pin mana yang menjadi relay, mengonfigurasi Wi-Fi, dan mengisi alamat server MQTT Anda.
*   **ESPHome**: Menggunakan file konfigurasi berbasis teks sederhana (`.yaml`). Sangat canggih karena terintegrasi otomatis dengan **Home Assistant** (pusat kontrol smart home lokal).

### Apakah Athom Terkunci dengan Tasmota/ESPHome?
**Tidak.** Pihak Athom hanya mempermudah pembeli dengan memasang (*pre-install*) Tasmota atau ESPHome sejak dari pabrik agar pembeli yang menyukai ekosistem lokal tidak perlu repot melakukan proses *flashing* sendiri menggunakan kabel. 
Jika suatu saat Anda berubah pikiran, Anda tetap bisa menghapus Tasmota/ESPHome tersebut dan mengunggah kode C++ (Arduino IDE) atau Rust buatan Anda sendiri ke dalam perangkat Athom tersebut.

