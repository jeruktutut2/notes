package services

import (
	"context"
	"fmt"
	"note-golang-mongodb/helpers"
	modelentities "note-golang-mongodb/models/entitites"
	modelrequests "note-golang-mongodb/models/requests"
	modelresponses "note-golang-mongodb/models/responses"
	"note-golang-mongodb/repositories"
	"note-golang-mongodb/utils"

	"go.mongodb.org/mongo-driver/bson/primitive"
)

type MongodbService interface {
	Create(ctx context.Context, createRequest modelrequests.CreateRequest) (response modelresponses.Response)
	Get(ctx context.Context, test string) (response modelresponses.Response)
	GetById(ctx context.Context, id string) (response modelresponses.Response)
	UpdateOne(ctx context.Context, updateRequest modelrequests.UpdateRequest) (response modelresponses.Response)
	UpdateById(ctx context.Context, updateRequest modelrequests.UpdateRequest) (response modelresponses.Response)
	DeleteOne(ctx context.Context, deleteRequest modelrequests.DeleteRequest) (response modelresponses.Response)
}

type mongodbService struct {
	MongoUtil         utils.MongoUtil
	UuidHelper        helpers.UuidHelper
	MongodbRepository repositories.MongodbRepository
}

func NewMongodbService(mongoUtil utils.MongoUtil, uuidHelper helpers.UuidHelper, mongodbRepository repositories.MongodbRepository) MongodbService {
	return &mongodbService{
		MongoUtil:         mongoUtil,
		UuidHelper:        uuidHelper,
		MongodbRepository: mongodbRepository,
	}
}

func (service *mongodbService) Create(ctx context.Context, createRequest modelrequests.CreateRequest) (response modelresponses.Response) {
	var test1 modelentities.Test1
	test1.Id = primitive.NewObjectID()
	test1.Test = createRequest.Test
	err := service.MongodbRepository.Create(service.MongoUtil.GetDb(), ctx, test1)
	if err != nil {
		fmt.Println("err:", err)
		return modelresponses.SetInternalServerErrorResponse()
	}
	return modelresponses.SetCreatedResponse(modelresponses.SetCreateResponse(test1))
}

func (service *mongodbService) Get(ctx context.Context, test string) (response modelresponses.Response) {
	test1s, err := service.MongodbRepository.Get(service.MongoUtil.GetDb(), ctx, test)
	if err != nil {
		fmt.Println("err:", err)
		return modelresponses.SetInternalServerErrorResponse()
	}
	return modelresponses.SetOkResponse(modelresponses.SetGetResponses(test1s))
}

func (service *mongodbService) GetById(ctx context.Context, id string) (response modelresponses.Response) {
	objectId, err := primitive.ObjectIDFromHex(id)
	if err != nil {
		fmt.Println("err:", err)
		return modelresponses.SetInternalServerErrorResponse()
	}
	test1, err := service.MongodbRepository.GetById(service.MongoUtil.GetDb(), ctx, objectId)
	if err != nil {
		fmt.Println("err:", err)
		return modelresponses.SetInternalServerErrorResponse()
	}
	return modelresponses.SetOkResponse(modelresponses.SetGetResponse(test1))
}

func (service *mongodbService) UpdateOne(ctx context.Context, updateRequest modelrequests.UpdateRequest) (response modelresponses.Response) {
	id, err := primitive.ObjectIDFromHex(updateRequest.Id)
	if err != nil {
		fmt.Println("err:", err)
		return modelresponses.SetInternalServerErrorResponse()
	}
	var test1 modelentities.Test1
	test1.Id = id
	test1.Test = updateRequest.Test
	rowsAffected, err := service.MongodbRepository.UpdateOne(service.MongoUtil.GetDb(), ctx, test1)
	if err != nil {
		fmt.Println("err:", err)
		return modelresponses.SetInternalServerErrorResponse()
	}
	fmt.Println("rowsAffected:", rowsAffected)
	return modelresponses.SetOkResponse(modelresponses.SetUpdateResponse(test1))
}

func (service *mongodbService) UpdateById(ctx context.Context, updateRequest modelrequests.UpdateRequest) (response modelresponses.Response) {
	id, err := primitive.ObjectIDFromHex(updateRequest.Id)
	if err != nil {
		fmt.Println("err:", err)
		return modelresponses.SetInternalServerErrorResponse()
	}

	var test1 modelentities.Test1
	test1.Id = id
	test1.Test = updateRequest.Test
	rowsAffected, err := service.MongodbRepository.UpdateById(service.MongoUtil.GetDb(), ctx, test1)
	if err != nil {
		fmt.Println("err:", err)
		return modelresponses.SetInternalServerErrorResponse()
	}
	fmt.Println("rowsAffected:", rowsAffected)
	return modelresponses.SetOkResponse(modelresponses.SetUpdateResponse(test1))
}

func (service *mongodbService) DeleteOne(ctx context.Context, deleteRequest modelrequests.DeleteRequest) (response modelresponses.Response) {
	objectId, err := primitive.ObjectIDFromHex(deleteRequest.Id)
	if err != nil {
		fmt.Println("err:", err)
		return modelresponses.SetInternalServerErrorResponse()
	}
	rowsAffected, err := service.MongodbRepository.DeleteOne(service.MongoUtil.GetDb(), ctx, objectId)
	if err != nil {
		fmt.Println("err:", err)
		return modelresponses.SetInternalServerErrorResponse()
	}
	fmt.Println("rowsAffected:", rowsAffected)
	return modelresponses.SetNoContentResponse()
}
