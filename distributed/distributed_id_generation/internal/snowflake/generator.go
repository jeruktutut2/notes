package snowflake

import (
	"log"

	"github.com/bwmarrin/snowflake"
)

type IDGenerator struct {
	node *snowflake.Node
}

// NewIDGenerator membuat instance generator dengan ID Node (Machine ID) unik.
// Di sistem terdistribusi nyata, nodeID ini harus unik per instance/server (bisa diinject via env var).
func NewIDGenerator(nodeID int64) *IDGenerator {
	node, err := snowflake.NewNode(nodeID)
	if err != nil {
		log.Fatalf("Gagal membuat Snowflake node: %v", err)
	}

	return &IDGenerator{
		node: node,
	}
}

// GenerateID menghasilkan integer 64-bit yang unik.
func (g *IDGenerator) GenerateID() int64 {
	return g.node.Generate().Int64()
}
