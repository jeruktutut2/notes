package utils

import (
	"context"
	"log"
	"time"

	"github.com/redis/go-redis/v9"
)

type RedisUtil interface {
	GetClient() *redis.Client
	Close(host string, port string)
	Set(ctx context.Context, key string, value interface{}, expiration time.Duration) (string, error)
	Get(ctx context.Context, key string) (string, error)
	Del(ctx context.Context, key string) (int64, error)
}

type redisUtil struct {
	Client *redis.Client
}

func NewRedisUtil(host string, port string, database int) RedisUtil {
	println(time.Now().String()+" redis: connecting to ", host+":"+port)
	rdb := redis.NewClient(&redis.Options{
		Addr:     host + ":" + port,
		Password: "",       // no password set
		DB:       database, // use default DB
	})
	println(time.Now().String()+" redis: connected to", host+":"+port)

	println(time.Now().String()+" redis: pinging to ", host+":"+port)
	ctx := context.Background()
	_, err := rdb.Ping(ctx).Result()
	if err != nil {
		log.Fatalln("redis: error when pinging to:", err)
	}
	println(time.Now().String()+" redis: pinged to ", host+":"+port)

	return &redisUtil{
		Client: rdb,
	}
}

func (util *redisUtil) GetClient() *redis.Client {
	return util.Client
}

func (util *redisUtil) Close(host string, port string) {
	println(time.Now().String()+" redis: closing to ", host+":"+port)
	err := util.Client.Close()
	if err != nil {
		log.Fatalln("redis close connection error:", err)
	}
	println(time.Now().String()+" redis: closed to ", host+":"+port)
}

func (util *redisUtil) Set(ctx context.Context, key string, value interface{}, expiration time.Duration) (string, error) {
	return util.Client.Set(ctx, key, value, expiration).Result()
}

func (util *redisUtil) Get(ctx context.Context, key string) (string, error) {
	return util.Client.Get(ctx, key).Result()
}

func (util *redisUtil) Del(ctx context.Context, key string) (int64, error) {
	return util.Client.Del(ctx, key).Result()
}
