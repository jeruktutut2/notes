package modelresponses

import modelentities "note-golang-mongodb/models/entitites"

type UpdateResponse struct {
	Id   string `json:"id"`
	Test string `json:"test"`
}

func SetUpdateResponse(test1 modelentities.Test1) UpdateResponse {
	return UpdateResponse{
		Id:   test1.Id.Hex(),
		Test: test1.Test,
	}
}
