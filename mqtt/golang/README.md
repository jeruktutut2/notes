# MQTT

## library
    go get github.com/labstack/echo/v4
    go get github.com/eclipse/paho.mqtt.golang

## instruction
1. create folder ```mosquitto```
2. create configuration file ```mosquitto.conf``` inside ```monsquitto/config```
3. (optional) if you want to set authentication, set
    docker run --rm -it eclipse-mosquitto mosquitto_passwd -c /mosquitto/config/password_file <username>
    and add 
    password_file /mosquitto/config/password_file
    allow_anonymous false
    in ```mosquitto.conf```
4. make sure to set allow_anonymous to ```false``` when it is in production
5. run docker compose using ```docker-compose up -d``` or ```docker compose up -d``` or ```docker run --name project-mosquitto -it -p 1883:1883 -p 9001:9001 -v "./mosquitto/config:/mosquitto/config" eclipse-mosquitto:latest``` or ```docker run --name project-mosquitto -it -p 1883:1883 -p 9001:9001 -v "$PWD/mosquitto/config:/mosquitto/config" eclipse-mosquitto:latest``` or ```docker run -it -p 1883:1883 -v "$PWD/mosquitto/config:/mosquitto/config" -v /mosquitto/data -v /mosquitto/log eclipse-mosquitto```

6. check log using ```docker logs mosquitto```
7. access it through ```localhost:1883```

## addional
    docker run --rm -it eclipse-mosquitto mosquitto_passwd -c /mosquitto/config/password_file <username>
1. docker run --rm: Menjalankan container sementara dan langsung menghapusnya setelah selesai.
2. -it: run container interactivelly
3. eclipse-mosquitto: the image docker.
4. mosquitto_passwd: Tool (mosquitto) to create and manage password_file.
5. -c: to create new file to save username and password. If file already exists, that file will be replaced.
6. /mosquitto/config/password_file: location of password_file inside configuration folder.
7. <username>: Username that you want to use (e.g admin).

## prompt password
1. if you use ```docker run --rm -it eclipse-mosquitto mosquitto_passwd -c /mosquitto/config/password_file <username>```, after entering that command, you will be asked the password, please enter the password, (username = root : password = 12345)
2. if you dont want to use it, use batch instead
    docker run --rm -it -v $(pwd)/mosquitto/config:/mosquitto/config eclipse-mosquitto mosquitto_passwd -b /mosquitto/config/password_file admin mypassword


## subscribe to topic
    mosquitto_sub -h localhost -t "test/topic"

## publish to topic
    mosquitto_pub -h localhost -t "test/topic" -m "Hello MQTT"

## docker
    docker inspect project-mosquitto