package services

import (
	"fmt"
	"note-golang-memcached/utils"

	"github.com/bradfitz/gomemcache/memcache"
)

type MemcachedService interface {
	Set(key string, value string) (response string)
	Get(key string) (response string)
	Delete(key string) (response string)
}

type memcachedService struct {
	MemcachedUtil utils.MemcachedUtil
}

func NewMemcachedService(memcachedUtil utils.MemcachedUtil) MemcachedService {
	return &memcachedService{
		MemcachedUtil: memcachedUtil,
	}
}

func (service *memcachedService) Set(key string, value string) (response string) {
	err := service.MemcachedUtil.GetClient().Set(&memcache.Item{Key: key, Value: []byte(value)})
	if err != nil {
		fmt.Println("error when saving:", err)
	}
	response = "success"
	return
}

func (service *memcachedService) Get(key string) (response string) {
	item, err := service.MemcachedUtil.GetClient().Get(key)
	if err != nil {
		if err == memcache.ErrCacheMiss {
			fmt.Println("no cache with key:", key)
			return
		}
		fmt.Println("error when getting cache:", err)
		return
	}
	fmt.Println("item:", item.Key, string(item.Value))
	response = "success"
	return
}

func (service *memcachedService) Delete(key string) (response string) {
	err := service.MemcachedUtil.GetClient().Delete(key)
	if err != nil {
		if err == memcache.ErrCacheMiss {
			fmt.Println("no cache with key:", err)
			return
		}
		fmt.Println("error when delete cache:", err)
	}
	response = "success"
	return
}
