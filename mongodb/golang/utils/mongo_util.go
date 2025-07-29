package utils

import (
	"context"
	"log"
	"time"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type MongoUtil interface {
	GetDb() *mongo.Database
	Close(host string, port string)
}

type mongoUtil struct {
	client *mongo.Client
	db     *mongo.Database
}

func NewMongoDbConnection(host string, username string, password string, database string, port string, maxPoolSize uint64, minPoolSize uint64, maxConnIdleTime int) MongoUtil {
	println(time.Now().String(), "mongodb: connecting to", host+":"+port)
	uri := "mongodb://" + username + ":" + password + "@" + host + ":" + port
	clientOptions := options.Client().ApplyURI(uri).SetMaxPoolSize(maxPoolSize).SetMinPoolSize(minPoolSize).SetMaxConnIdleTime(time.Duration(maxConnIdleTime) * time.Second)
	client, err := mongo.Connect(context.Background(), clientOptions)
	if err != nil {
		log.Fatalln("error when connecting mongodb:", err)
	}
	println(time.Now().String(), "mongodb: connected to", host+":"+port)

	println(time.Now().String(), "mongodb: pinging to", host+":"+port)
	err = client.Ping(context.Background(), nil)
	if err != nil {
		log.Fatalln("error when pinging mongodb:", err)
	}
	println(time.Now().String(), "mongodb: pinged to", host+":"+port)

	return &mongoUtil{
		client: client,
		db:     client.Database(database),
	}
}

func (util *mongoUtil) GetDb() *mongo.Database {
	return util.db
}

func (util *mongoUtil) Close(host string, port string) {
	println(time.Now().String(), "mongodb: closing to", host+":"+port)
	err := util.client.Disconnect(context.Background())
	if err != nil {
		log.Fatalln("error when closing mongo:", err)
	}
	println(time.Now().String(), "mongodb: closed to", host+":"+port)
}
