# KAFKA

## library
    go get github.com/labstack/echo/v4
    go get github.com/confluentinc/confluent-kafka-go

## docker
    docker-compose up -d
    docker-compose -f docker-compose_1.yml up -d
    docker-compose down
    docker-compose -f docker-compose_1.yml down

## topic
    create email topic: kafka-topics --bootstrap-server localhost:9092 --create --topic email
    create text-message topic: kafka-topics --bootstrap-server localhost:9092 --create --topic text-message
    show list topic: kafka-topics --bootstrap-server localhost:9092 --list
    show list topic: kafka-topics --bootstrap-server kafka1:9092 --list
    create email topic: kafka-topics --bootstrap-server kafka1:9092 --create --topic email
    create text message topic: kafka-topics --bootstrap-server kafka1:9092 --create --topic text-message

## producer and consumer
    producer email: kafka-console-producer --broker-list localhost:9092 --topic email
    producer text-message: kafka-console-producer --broker-list localhost:9092 --topic text-message
    consumer email: kafka-console-consumer --bootstrap-server localhost:9092 --topic email
    consumer text-message: kafka-console-consumer --bootstrap-server localhost:9092 --topic text-message
    consumer group email: kafka-console-consumer --bootstrap-server localhost:9092 --topic email --group email-consumer-group
    consumer group text-message text-message-consumer-group-table: kafka-console-consumer --bootstrap-server localhost:9092 --topic email --group text-message-consumer-group

## link
    https://www.conduktor.io/kafka/how-to-start-kafka-using-docker/
    https://github.com/conduktor/kafka-stack-docker-compose
    docker-compose -f zk-single-kafka-single.yml up -d
