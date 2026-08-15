# Panduan Praktis Memprogram Mikrokontroler (ESP8266/ESP32)

Berikut adalah langkah-langkah praktis untuk memprogram mikrokontroler menggunakan **C++ (Arduino IDE)**, yang merupakan metode paling mudah dan populer untuk membuat lampu pintar.

---

## Langkah 1: Persiapan Alat dan Software
1.  **Download Arduino IDE**: Unduh dan instal versi terbaru dari website resmi [arduino.cc](https://www.arduino.cc/en/software).
2.  **Kabel Data USB**: Pastikan Anda menggunakan kabel USB yang mendukung **transfer data**, bukan hanya kabel charger biasa (karena banyak kabel murah yang hanya bisa menghantarkan daya tanpa jalur data).
3.  **Driver USB to UART**: Mikrokontroler menggunakan chip komunikasi seperti CH340, CP2102, atau FTDI. Jika komputer Anda tidak mendeteksi port USB mikrokontroler, unduh dan instal driver chip tersebut (biasanya CH340 untuk NodeMCU versi murah).

---

## Langkah 2: Konfigurasi Arduino IDE untuk ESP8266 / ESP32
Secara default, Arduino IDE hanya mendukung papan Arduino resmi (seperti Arduino Uno). Kita perlu menambahkan dukungan untuk chip ESP:

1.  Buka Arduino IDE, lalu masuk ke **File** -> **Preferences** (di Mac: **Arduino IDE** -> **Settings**).
2.  Pada kolom **Additional Boards Manager URLs**, masukkan URL berikut:
    *   **Untuk ESP8266**: `http://arduino.esp8266.com/stable/package_esp8266com_index.json`
    *   **Untuk ESP32**: `https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json`
    *(Jika ingin memasukkan keduanya, pisahkan dengan tanda koma)*.
3.  Klik **OK**.
4.  Masuk ke menu **Tools** -> **Board** -> **Boards Manager...**
5.  Cari `esp8266` atau `esp32`, lalu klik **Install**.

---

## Langkah 3: Membuat Kode Program (Web Server Lokal Sederhana)
Hubungkan mikrokontroler ke komputer menggunakan kabel USB. Buat sketch baru di Arduino IDE, lalu gunakan kode contoh di bawah ini (contoh menggunakan **ESP8266/NodeMCU**):

```cpp
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>

// Konfigurasi Wi-Fi Rumah Anda
const char* ssid = "NAMA_WIFI_ANDA";
const char* password = "PASSWORD_WIFI_ANDA";

// Definisikan Pin Relay (Sesuaikan dengan koneksi Anda)
const int relayPin = 14; // Pin D5 pada NodeMCU

ESP8266WebServer server(80);

// Halaman utama
void handleRoot() {
  String html = "<html><body>";
  html += "<h1>Kontrol Lampu Pintar</h1>";
  html += "<p><a href=\"/on\"><button style=\"font-size:20px; background-color:green; color:white;\">Nyalakan Lampu</button></a></p>";
  html += "<p><a href=\"/off\"><button style=\"font-size:20px; background-color:red; color:white;\">Matikan Lampu</button></a></p>";
  html += "</body></html>";
  server.send(200, "text/html", html);
}

// Handler untuk menyalakan lampu
void handleLampuOn() {
  digitalWrite(relayPin, LOW); // Catatan: Beberapa modul relay aktif saat LOW (Active Low)
  server.send(200, "text/html", "Lampu ON. <a href=\"/\">Kembali</a>");
}

// Handler untuk mematikan lampu
void handleLampuOff() {
  digitalWrite(relayPin, HIGH); // Relay mati saat HIGH
  server.send(200, "text/html", "Lampu OFF. <a href=\"/\">Kembali</a>");
}

void setup() {
  Serial.begin(115200);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH); // Default: Lampu Mati

  // Koneksi ke Wi-Fi
  WiFi.begin(ssid, password);
  Serial.println("");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Terhubung ke Wi-Fi dengan IP: ");
  Serial.println(WiFi.localIP());

  // Rute Web Server
  server.on("/", handleRoot);
  server.on("/on", handleLampuOn);
  server.on("/off", handleLampuOff);

  server.begin();
  Serial.println("Web server aktif!");
}

void loop() {
  server.handleClient();
}
```

---

## Langkah 4: Upload Program
1.  Pilih Papan (*Board*) Anda di **Tools** -> **Board** -> **ESP8266 Boards** -> **NodeMCU 1.0 (ESP-12E Module)** (atau sesuaikan dengan board Anda).
2.  Pilih Port USB yang aktif di **Tools** -> **Port** (Contoh: `/dev/cu.usbserial-...` di Mac, atau `COM3` di Windows).
3.  Klik tombol **Upload** (ikon panah kanan di pojok kiri atas).
4.  Tunggu hingga proses kompilasi dan upload selesai (muncul tulisan `Done uploading`).

---

## Langkah 5: Cara Mengontrol Lewat HP
1.  Buka **Serial Monitor** di Arduino IDE (**Tools** -> **Serial Monitor**) dan atur baud rate ke `115200`.
2.  Tekan tombol RST/RESET pada mikrokontroler. Anda akan melihat proses koneksi Wi-Fi dan alamat IP yang didapatkan (misalnya: `192.168.1.15`).
3.  Pastikan HP Anda terhubung ke Wi-Fi yang sama dengan mikrokontroler.
4.  Buka browser di HP (Chrome/Safari), ketik alamat IP tersebut (`192.168.1.15`).
5.  Halaman web dengan tombol kontrol lampu akan muncul, dan Anda bisa menyalakan atau mematikan lampu langsung dari HP!
