# NOTE GOLANG RABBITMQ

## library
    go get github.com/labstack/echo/v4
    go get github.com/rabbitmq/amqp091-go

## docker 
    docker run -d --hostname my-rabbit --name rabbitmq-note -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password -p 15672:15672 -p 5672:5672 rabbitmq:3-management

## env
    export RABBITMQ_HOST=localhost
    export RABBITMQ_USERNAME=user
    export RABBITMQ_PASSWORD=password
    export RABBITMQ_PORT=5672

## access
    http://localhost:15672/#/ sign in as user = user : password = password
    web management: localhost:15672
    rabbitmq port: localhost: 5672
    before using rabbitmq, please create exchange, create queue and tie it using bindings
    create exchange (notification) - create queue (email or text-message) - create bindings


## ConsumeWithContext
1. queue string
    Nama queue dari mana pesan akan dikonsumsi. Queue ini harus sudah ada sebelumnya atau dibuat menggunakan deklarasi queue.
    Contoh nilai: "my-queue"

2. consumer string
    Nama unik untuk konsumen yang membaca pesan dari queue. Biasanya ini digunakan untuk identifikasi konsumen tertentu.
    Contoh nilai: "my-consumer"

3. autoAck bool
    Menentukan apakah acknowledgment (konfirmasi) untuk pesan diterima secara otomatis oleh server RabbitMQ.
    true: Pesan langsung diakui oleh server saat diterima oleh konsumen.
    false: Konsumen harus secara eksplisit mengakui pesan menggunakan Delivery.Ack() atau Delivery.Nack().
    Contoh nilai: false
    (Disarankan false agar dapat mengontrol kapan pesan dianggap selesai diproses.)

4. exclusive bool
    Menentukan apakah queue akan dikonsumsi secara eksklusif oleh konsumen ini.
    true: Queue hanya dapat digunakan oleh konsumen ini.
    false: Queue dapat digunakan oleh beberapa konsumen.
    Contoh nilai: false

5. noLocal bool
    (Tidak didukung di RabbitMQ, hanya relevan untuk implementasi AMQP lainnya.)
    Menentukan apakah pesan yang diterbitkan oleh konsumen yang sama tidak akan dikirim kembali ke konsumen itu sendiri.
    Contoh nilai: false

6. noWait bool
    Jika true, konsumen tidak akan menunggu respons dari server RabbitMQ untuk permintaan konsumsi ini. Jika ada kesalahan, konsumen tidak akan diberitahu. Biasanya disarankan untuk tetap menggunakan false.
    Contoh nilai: false

7. args amqp091.Table
    Argument tambahan dalam bentuk map yang dapat digunakan untuk mengatur parameter tambahan konsumsi. Biasanya tidak perlu mengisi ini kecuali ada kebutuhan spesifik.
    Contoh nilai: nil
    (atau amqp091.Table{"x-priority": int32(10)} untuk memberikan prioritas.)