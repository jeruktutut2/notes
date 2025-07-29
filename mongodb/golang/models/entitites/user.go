package modelentities

type User struct {
	Id       string `bson:"_id" json:"id"`
	Email    string `bson:"email" json:"email"`
	Password string `bson:"password" json:"password"`
}
