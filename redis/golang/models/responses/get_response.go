package modelresponses

import modelentities "note-golang-redis/models/entities"

type GetResponse struct {
	Id   string `json:"id"`
	Test string `json:"test"`
}

func SetGetResponse(test1 modelentities.Test1) GetResponse {
	return GetResponse{
		Id:   test1.Id,
		Test: test1.Test,
	}
}
