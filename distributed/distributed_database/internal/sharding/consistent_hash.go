package sharding

import (
	"fmt"
	"hash/crc32"
	"sort"
	"strconv"
)

// ConsistentHash menyimpan cincin hash dan pemetaan node
type ConsistentHash struct {
	// hashKeys menyimpan nilai hash yang sudah diurutkan
	hashKeys []uint32
	// hashMap memetakan nilai hash (titik di cincin) ke nama Node (URL/ID)
	hashMap map[uint32]string
	// virtualNodes menentukan berapa banyak replika virtual untuk tiap node agar merata
	virtualNodes int
}

// NewConsistentHash membuat cincin baru
func NewConsistentHash(virtualNodes int) *ConsistentHash {
	return &ConsistentHash{
		hashMap:      make(map[uint32]string),
		virtualNodes: virtualNodes,
	}
}

// Add memasukkan Node (misal: "ServerA") ke dalam cincin
func (c *ConsistentHash) Add(node string) {
	for i := 0; i < c.virtualNodes; i++ {
		// Buat virtual node key, misal "ServerA#0", "ServerA#1"
		virtualKey := fmt.Sprintf("%s#%d", node, i)
		hash := crc32.ChecksumIEEE([]byte(virtualKey))
		
		c.hashKeys = append(c.hashKeys, hash)
		c.hashMap[hash] = node
	}
	
	// Cincin hash harus diurutkan (ascending) untuk binary search
	sort.Slice(c.hashKeys, func(i, j int) bool {
		return c.hashKeys[i] < c.hashKeys[j]
	})
}

// Get mencari Node mana yang berhak menyimpan data dengan 'key' tertentu
func (c *ConsistentHash) Get(key string) string {
	if len(c.hashKeys) == 0 {
		return ""
	}

	hash := crc32.ChecksumIEEE([]byte(key))

	// Binary search untuk mencari titik (node) terdekat SEARAH JARUM JAM
	// yang memiliki nilai hash lebih besar atau sama dengan hash data
	idx := sort.Search(len(c.hashKeys), func(i int) bool {
		return c.hashKeys[i] >= hash
	})

	// Jika data melewati titik terakhir di cincin, putar balik ke titik pertama
	if idx == len(c.hashKeys) {
		idx = 0
	}

	return c.hashMap[c.hashKeys[idx]]
}

// Remove menghapus Node (beserta virtual node-nya) dari cincin
func (c *ConsistentHash) Remove(node string) {
	for i := 0; i < c.virtualNodes; i++ {
		virtualKey := strconv.Itoa(i) + node
		hash := crc32.ChecksumIEEE([]byte(virtualKey))
		
		delete(c.hashMap, hash)
		
		// Hapus dari slice hashKeys
		for j, k := range c.hashKeys {
			if k == hash {
				c.hashKeys = append(c.hashKeys[:j], c.hashKeys[j+1:]...)
				break
			}
		}
	}
}
