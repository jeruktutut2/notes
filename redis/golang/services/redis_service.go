package services

import (
	"context"
	"encoding/json"
	modelentities "note-golang-redis/models/entities"
	modelrequests "note-golang-redis/models/requests"
	modelresponses "note-golang-redis/models/responses"
	"note-golang-redis/utils"

	"github.com/google/uuid"
	"github.com/redis/go-redis/v9"
)

type RedisService interface {
	Set(ctx context.Context, createRequest modelrequests.CreateRequest) (response modelresponses.Response)
	Get(ctx context.Context, key string) (response modelresponses.Response)
	Del(ctx context.Context, deleteRequest modelrequests.DeleteRequest) (esponse modelresponses.Response)
}

type redisService struct {
	RedisUtil utils.RedisUtil
}

func NewRedisService(redisUtil utils.RedisUtil) RedisService {
	return &redisService{
		RedisUtil: redisUtil,
	}
}

func (service *redisService) Set(ctx context.Context, createRequest modelrequests.CreateRequest) (response modelresponses.Response) {
	var test1 modelentities.Test1
	test1.Id = uuid.NewString()
	test1.Test = createRequest.Test
	resultBytes, err := json.Marshal(test1)
	if err != nil {
		// return modelresponses.SetHttpResponse(http.StatusInternalServerError, nil, []modelresponses.Error{{Field: "message", Message: "internal server error"}})
		return modelresponses.SetInternalServerErrorResponse()
	}
	// _, err = service.RedisUtil.Set(ctx, test1.Id, string(resultBytes), time.Duration(10)*time.Second)
	_, err = service.RedisUtil.Set(ctx, test1.Id, string(resultBytes), 0)
	if err != nil {
		// return modelresponses.SetHttpResponse(http.StatusInternalServerError, nil, []modelresponses.Error{{Field: "message", Message: "internal server error"}})
		return modelresponses.SetInternalServerErrorResponse()
	}
	// return modelresponses.SetHttpResponse(http.StatusCreated, createRequest, []modelresponses.Error{})
	return modelresponses.SetCreatedResponse(modelresponses.SetCreateResponse(test1))

}

func (service *redisService) Get(ctx context.Context, key string) (response modelresponses.Response) {
	result, err := service.RedisUtil.Get(ctx, key)
	if err != nil {
		if err == redis.Nil {
			return modelresponses.SetNotFoundResponse("cannot find test1 with id: " + key)
		}
		// return modelresponses.SetHttpResponse(http.StatusInternalServerError, nil, []modelresponses.Error{{Field: "message", Message: "internal server error"}})
		return modelresponses.SetInternalServerErrorResponse()
	}
	// var createRequest modelrequests.CreateRequest
	var test1 modelentities.Test1
	err = json.Unmarshal([]byte(result), &test1)
	if err != nil {
		// return modelresponses.SetHttpResponse(http.StatusInternalServerError, nil, []modelresponses.Error{{Field: "message", Message: "internal server error"}})
		return modelresponses.SetInternalServerErrorResponse()
	}
	// return modelresponses.SetHttpResponse(http.StatusOK, createRequest, []modelresponses.Error{})
	return modelresponses.SetOkResponse(modelresponses.SetGetResponse(test1))
}

func (service *redisService) Del(ctx context.Context, deleteRequest modelrequests.DeleteRequest) (response modelresponses.Response) {
	rowsAffected, err := service.RedisUtil.Del(ctx, deleteRequest.Id)
	if err != nil {
		// return modelresponses.SetHttpResponse(http.StatusInternalServerError, nil, []modelresponses.Error{{Field: "message", Message: "internal server error"}})
		return modelresponses.SetInternalServerErrorResponse()
	} else if rowsAffected != 1 {
		// return modelresponses.SetHttpResponse(http.StatusInternalServerError, nil, []modelresponses.Error{{Field: "message", Message: "internal server error"}})
		return modelresponses.SetInternalServerErrorResponse()
	}
	// return modelresponses.SetHttpResponse(http.StatusNoContent, nil, []modelresponses.Error{})
	return modelresponses.SetNoContentResponse()
}
