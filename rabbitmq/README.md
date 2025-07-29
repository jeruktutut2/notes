# RABBITMQ

## curl test
    curl -i -X POST \
        -H "Content-Type: application/json" \
        -d '{"test": "test post"}' \
        http://localhost:8080/api/v1/message/send-message
    curl -i -X GET http://localhost:8080/rabbitmq/send-message/message1

## link
    https://www.rabbitmq.com/tutorials/tutorial-one-rust-stream please read this before doing stream

## docker
    docker run -it --rm --name rabbitmq-note -p 5552:5552 -p 15672:15672 -p 5672:5672 -e RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS='-rabbitmq_stream advertised_host localhost' rabbitmq:4-management

    docker run -d --hostname my-rabbit --name rabbitmq-note -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password -e RABBITMQ_SERVER_ADDITIONAL_ERL_ARGS='-rabbitmq_stream advertised_host localhost' -p 5552:5552 -p 15672:15672 -p 5672:5672 rabbitmq:4-management

    docker exec rabbitmq-note rabbitmq-plugins enable rabbitmq_stream rabbitmq_stream_management 