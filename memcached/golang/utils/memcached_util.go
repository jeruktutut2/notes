package utils

import (
	"log"
	"time"

	"github.com/bradfitz/gomemcache/memcache"
)

type MemcachedUtil interface {
	GetClient() *memcache.Client
	Close()
}

type memcachedUtil struct {
	Client *memcache.Client
}

func NewMemcachedUtil() MemcachedUtil {
	println(time.Now().String(), "memcached: connecting")
	client := memcache.New("localhost:11211")
	println(time.Now().String(), "memcached: connected")

	println(time.Now().String(), "memcached: pinging")
	err := client.Ping()
	if err != nil {
		log.Fatalln("error when pinging:", err)
	}
	println(time.Now().String(), "memcached: pinged")
	return &memcachedUtil{
		Client: client,
	}
}

func (util *memcachedUtil) GetClient() *memcache.Client {
	return util.Client
}

func (util *memcachedUtil) Close() {
	println(time.Now().String(), "memcached: closing")
	err := util.Client.Close()
	if err != nil {
		log.Fatalln("error when closing memcached:", err)
	}
	println(time.Now().String(), "memcached: closed")
}
