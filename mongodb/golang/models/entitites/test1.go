package modelentities

import "go.mongodb.org/mongo-driver/bson/primitive"

type Test1 struct {
	Id   primitive.ObjectID `bson:"_id"`
	Test string             `bson:"test"`
}
