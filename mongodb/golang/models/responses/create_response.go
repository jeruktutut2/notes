package modelresponses

import modelentities "note-golang-mongodb/models/entitites"

type CreateResponse struct {
	Id   string `json:"id"`
	Test string `json:"test"`
}

func SetCreateResponse(test1 modelentities.Test1) CreateResponse {
	return CreateResponse{
		Id:   test1.Id.Hex(),
		Test: test1.Test,
	}
}
