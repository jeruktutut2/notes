package services

import (
	"context"
	"database/sql"
	"net/http"
	modelentities "note-golang-postgresql/models/entities"
	modelrequests "note-golang-postgresql/models/requests"
	modelresponses "note-golang-postgresql/models/responses"
	"note-golang-postgresql/repositories"
	"note-golang-postgresql/utils"
)

type PostgresService interface {
	Create(ctx context.Context, createRequest modelrequests.CreateRequest) (response modelresponses.Response)
	Get(ctx context.Context, id int) (response modelresponses.Response)
	Update(ctx context.Context, updateRequest modelrequests.UpdateRequest) (response modelresponses.Response)
	Delete(ctx context.Context, deleteRequest modelrequests.DeleteRequest) (response modelresponses.Response)
}

type postgresService struct {
	PostgresUtil       utils.PostgresUtil
	PostgresRepository repositories.PostgresRepository
}

func NewPostgresService(postgresUtil utils.PostgresUtil, postgresRepository repositories.PostgresRepository) PostgresService {
	return &postgresService{
		PostgresUtil:       postgresUtil,
		PostgresRepository: postgresRepository,
	}
}

func (service *postgresService) Create(ctx context.Context, createRequest modelrequests.CreateRequest) (response modelresponses.Response) {
	tx, err := service.PostgresUtil.BeginTxx(ctx, &sql.TxOptions{})
	if err != nil {
		return modelresponses.SetInternalServerErrorResponse()
	}

	defer func() {
		errCommitOrRollback := service.PostgresUtil.CommitOrRollback(tx, err)
		if errCommitOrRollback != nil {
			response = modelresponses.SetInternalServerErrorResponse()
		}
	}()

	// var user modelentities.User
	// user.Email = createRequest.Email
	// user.Password = createRequest.Password
	var test1 modelentities.Test1
	test1.Test = createRequest.Test
	id, err := service.PostgresRepository.Create(tx, ctx, test1)
	if err != nil {
		return modelresponses.SetInternalServerErrorResponse()
	}
	// user.Id = id
	test1.Id = id
	// modelresponses.SetDataHttpResponse(http.StatusCreated, test1)
	return modelresponses.SetCreateResponse(test1)
}

func (service *postgresService) Get(ctx context.Context, id int) (response modelresponses.Response) {
	test1, err := service.PostgresRepository.Get(service.PostgresUtil.GetDb(), ctx, id)
	if err != nil {
		return modelresponses.SetInternalServerErrorResponse()
	}
	// modelresponses.SetDataHttpResponse(http.StatusCreated, user)
	return modelresponses.SetOkResponse(test1)
}

func (service *postgresService) Update(ctx context.Context, updateRequest modelrequests.UpdateRequest) (response modelresponses.Response) {
	tx, err := service.PostgresUtil.BeginTxx(ctx, &sql.TxOptions{})
	if err != nil {
		return modelresponses.SetInternalServerErrorResponse()
	}

	defer func() {
		errCommitOrRollback := service.PostgresUtil.CommitOrRollback(tx, err)
		if errCommitOrRollback != nil {
			response = modelresponses.SetInternalServerErrorResponse()
		}
	}()

	// var user modelentities.User
	// user.Id = updateRequest.Id
	// user.Email = updateRequest.Email
	// user.Password = updateRequest.Password
	var test1 modelentities.Test1
	test1.Id = updateRequest.Id
	test1.Test = updateRequest.Test
	rowsAffected, err := service.PostgresRepository.Update(tx, ctx, test1)
	if err != nil {
		return modelresponses.SetInternalServerErrorResponse()
	} else if rowsAffected != 1 {
		return modelresponses.SetResponse(http.StatusInternalServerError, nil, modelresponses.MessageResponse{Message: "rows affected not one"})
	}
	// modelresponses.SetDataHttpResponse(http.StatusCreated, user)
	return modelresponses.SetOkResponse(test1)
}

func (service *postgresService) Delete(ctx context.Context, deleteRequst modelrequests.DeleteRequest) (response modelresponses.Response) {
	tx, err := service.PostgresUtil.BeginTxx(ctx, &sql.TxOptions{})
	if err != nil {
		return modelresponses.SetInternalServerErrorResponse()
	}

	defer func() {
		errCommitOrRollback := service.PostgresUtil.CommitOrRollback(tx, err)
		if errCommitOrRollback != nil {
			response = modelresponses.SetInternalServerErrorResponse()
		}
	}()

	rowsAffected, err := service.PostgresRepository.Delete(tx, ctx, deleteRequst.Id)
	if err != nil {
		return modelresponses.SetInternalServerErrorResponse()
	} else if rowsAffected != 1 {
		return modelresponses.SetResponse(http.StatusInternalServerError, nil, modelresponses.MessageResponse{Message: "rows affected create mysql is not 1"})
	}
	// modelresponses.SetDataHttpResponse(http.StatusCreated, modelresponses.SetMessageHttpResponse("successfully delete user"))
	return modelresponses.SetNoContentResponse()
}
