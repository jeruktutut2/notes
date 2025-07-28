package modelentities

import (
	"database/sql"

	"github.com/google/uuid"
)

type Test1 struct {
	Id   uuid.NullUUID  `db:"id"`
	Test sql.NullString `db:"test1"`
}
