package modelresponses

import modelentities "note-golang-mongodb/models/entitites"

type GetResponse struct {
	Id   string `json:"id"`
	Test string `json:"test"`
}

func SetGetResponse(test1 modelentities.Test1) GetResponse {
	return GetResponse{
		Id:   test1.Id.Hex(),
		Test: test1.Test,
	}
}

func SetGetResponses(test1s []modelentities.Test1) (getResponses []GetResponse) {
	for _, test1 := range test1s {
		var getResponse GetResponse
		getResponse.Id = test1.Id.Hex()
		getResponse.Test = test1.Test
		getResponses = append(getResponses, getResponse)
	}
	return
}
