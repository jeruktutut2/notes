package utils

import (
	"log"
	"time"

	"github.com/rabbitmq/amqp091-go"
)

type RabbitmqUtil interface {
	GetConnection() *amqp091.Connection
	GetChannel() *amqp091.Channel
	Close(host string, port string)
}

type rabbitmqUtil struct {
	Connection *amqp091.Connection
	Channel    *amqp091.Channel
}

func NewRabbitmqConnection(host string, username string, password string, port string) RabbitmqUtil {
	println(time.Now().String(), "rabbitmq: connecting to "+host+":"+port)
	connection, err := amqp091.Dial("amqp://" + username + ":" + password + "@" + host + ":" + port + "/")
	if err != nil {
		log.Fatalln("error when connecting rabbitmq: ", err)
	}
	println(time.Now().String(), "rabbitmq: connected to "+host+":"+port)

	println(time.Now().String(), "rabbitmq: opening channel "+host+":"+port)
	channel, err := connection.Channel()
	if err != nil {
		log.Fatalln("error when opening channel:", err)
	}
	println(time.Now().String(), "rabbitmq: opened channel "+host+":"+port)

	return &rabbitmqUtil{
		Connection: connection,
		Channel:    channel,
	}
}

func (util *rabbitmqUtil) GetConnection() *amqp091.Connection {
	return util.Connection
}

func (util *rabbitmqUtil) GetChannel() *amqp091.Channel {
	return util.Channel
}

func (util *rabbitmqUtil) Close(host string, port string) {
	println(time.Now().String(), "rabbitmq: closing to "+host+":"+port)
	util.Connection.Close()
	println(time.Now().String(), "rabbitmq: closed to "+host+":"+port)
}
