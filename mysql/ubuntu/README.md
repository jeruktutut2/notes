# MYSQL

## Install
    sudo apt update
    sudo apt install mysql-server
    sudo systemctl status mysql
    sudo mysql_secure_installation
    Biasanya akan ditanya:
    set password root MySQL
    remove anonymous user → Y
    disallow remote root login → Y
    remove test database → Y
    reload privilege tables → Y

    sudo mysql
    sudo systemctl enable mysql

## uninstall
    Bonus – cara uninstall MySQL (kalau mau bersih)
    sudo apt remove --purge mysql-server mysql-client mysql-common mysql-server-core-* mysql-client-core-*
    sudo rm -rf /etc/mysql
    sudo rm -rf /var/lib/mysql
    sudo apt autoremove

## note
    melihat apakah login root pakai password atau plugin
    SELECT user, host, plugin
    FROM mysql.user
    WHERE user = 'root';

    Cek MySQL listen di alamat mana
    sudo ss -tlnp | grep 3306
    Artinya:
    Hasil	Makna
    127.0.0.1:3306	❌ hanya bisa dari server itu sendiri
    0.0.0.0:3306	✅ bisa menerima koneksi dari luar

    Cek konfigurasi bind-address
    Buka config:
    sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf

    Cari baris:
    bind-address = 127.0.0.1
    Kalau isinya:
    127.0.0.1
    👉 berarti MySQL hanya bisa diakses lokal
    Kalau:
    0.0.0.0
    atau barisnya di-comment:
    # bind-address = 127.0.0.1
    👉 berarti secara server, MySQL mengizinkan remote connection

    Cek user MySQL boleh login dari host mana
    Masuk ke MySQL:
    sudo mysql
    SELECT user, host FROM mysql.user;
    Artinya:
    host	Makna
    localhost	❌ hanya boleh dari server itu sendiri
    %	✅ boleh dari mana saja
    192.168.1.%	✅ hanya dari subnet tertentu

## user
    CREATE USER 'appuser'@'localhost' IDENTIFIED BY 'passwordku';
    GRANT ALL PRIVILEGES ON mydb.* TO 'appuser'@'localhost';
    FLUSH PRIVILEGES;
    SELECT user, host FROM mysql.user WHERE user = 'appuser';
    mysql -u appuser -p