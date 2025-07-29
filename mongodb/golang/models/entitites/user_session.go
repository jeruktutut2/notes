package modelentities

type UserUserSession struct {
	Id    string `bson:"_id"`
	Email string `bson:"email"`
}

type UserSession struct {
	Id                    string          `bson:"_id" json:"id"`
	User                  UserUserSession `bson:"user" json:"user"`
	AccessToken           string          `bson:"accessToken" json:"accessToken"`
	AccessTokenExpiredAt  int64           `bson:"accessTokenExpiredAt" json:"accessTokenExpiredAt"`
	RefreshToken          string          `bson:"refreshToken" json:"refreshToken"`
	RefreshTokenExpiredAt int64           `bson:"refreshTokenExpiredAt" json:"refreshTokenExpiredAt"`
	Ip                    string          `bson:"ip" json:"ip"`
	UserAgent             string          `bson:"userAgent" json:"userAgent"`
}
