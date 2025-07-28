package services

import (
	"context"
	"database/sql"
	"fmt"
	modelentities "note-golang-cockroachdb/models/entities"
	modelrequests "note-golang-cockroachdb/models/requests"
	modelresponses "note-golang-cockroachdb/models/responses"
	"note-golang-cockroachdb/repositories"
	"note-golang-cockroachdb/utils"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
)

type Test1Service interface {
	Create(ctx context.Context, createRequest modelrequests.CreateRequest) (response modelresponses.Response)
	GetById(ctx context.Context, id string) (response modelresponses.Response)
	GetAll(ctx context.Context) (response modelresponses.Response)
	Update(ctx context.Context, updateRequest modelrequests.UpdateRequest) (response modelresponses.Response)
	Delete(ctx context.Context, deleteRequest modelrequests.DeleteRequest) (response modelresponses.Response)
}

type test1Service struct {
	cockroachDbUtil utils.CockroachDbUtil
	test1Repository repositories.Test1Repository
}

func NewTest1Service(cockroachDbUtil utils.CockroachDbUtil, test1Repository repositories.Test1Repository) Test1Service {
	return &test1Service{
		cockroachDbUtil: cockroachDbUtil,
		test1Repository: test1Repository,
	}
}

func (service *test1Service) Create(ctx context.Context, createRequest modelrequests.CreateRequest) (response modelresponses.Response) {
	tx, err := service.cockroachDbUtil.BeginTx(ctx, pgx.TxOptions{})
	if err != nil {
		return modelresponses.SetInternalServerErrorResponse()
	}

	defer func() {
		errCommitOrRollback := service.cockroachDbUtil.CommitOrRollback(tx, ctx, err)
		if errCommitOrRollback != nil {
			response = modelresponses.SetInternalServerErrorResponse()
		}
	}()

	var test1 modelentities.Test1
	uuidv7, err := uuid.NewV7()
	if err != nil {
		return modelresponses.SetInternalServerErrorResponse()
	}
	test1.Id = uuid.NullUUID{Valid: true, UUID: uuidv7}
	test1.Test = sql.NullString{Valid: true, String: createRequest.Test}
	rowsAffected, err := service.test1Repository.Create(tx, ctx, test1)
	if err != nil {
		return modelresponses.SetInternalServerErrorResponse()
	}
	fmt.Println("rowsAffected:", rowsAffected)
	return modelresponses.SetCreateResponse(test1)
}

func (service *test1Service) GetById(ctx context.Context, id string) (response modelresponses.Response) {
	uuidv7, err := uuid.Parse(id)
	if err != nil {
		fmt.Println("err parse uuid getbyid service:", id, err)
		return modelresponses.SetInternalServerErrorResponse()
	}
	test1, err := service.test1Repository.GetById(service.cockroachDbUtil.GetDb(), ctx, uuidv7)
	if err != nil {
		fmt.Println("err getbyid service:", err)
		return modelresponses.SetInternalServerErrorResponse()
	}
	return modelresponses.SetOkResponse(test1)
}

func (service *test1Service) GetAll(ctx context.Context) (response modelresponses.Response) {
	test1s, err := service.test1Repository.GetAll(service.cockroachDbUtil.GetDb(), ctx)
	if err != nil {
		fmt.Println("err getall service:", err)
		return modelresponses.SetInternalServerErrorResponse()
	}
	return modelresponses.SetOkResponse(test1s)
}

func (service *test1Service) Update(ctx context.Context, updateRequest modelrequests.UpdateRequest) (response modelresponses.Response) {
	tx, err := service.cockroachDbUtil.BeginTx(ctx, pgx.TxOptions{})
	if err != nil {
		return modelresponses.SetInternalServerErrorResponse()
	}
	defer func() {
		errCommitOrRollback := service.cockroachDbUtil.CommitOrRollback(tx, ctx, err)
		if errCommitOrRollback != nil {
			response = modelresponses.SetInternalServerErrorResponse()
		}
	}()

	var test1 modelentities.Test1
	test1.Id = uuid.NullUUID{Valid: true, UUID: updateRequest.Id}
	test1.Test = sql.NullString{Valid: true, String: updateRequest.Test}
	rowsAffected, err := service.test1Repository.Update(tx, ctx, test1)
	if err != nil {
		return modelresponses.SetInternalServerErrorResponse()
	}
	fmt.Println("rowsAffected:", rowsAffected)
	return modelresponses.SetOkResponse(test1)
}

func (service *test1Service) Delete(ctx context.Context, deleteRequest modelrequests.DeleteRequest) (response modelresponses.Response) {
	tx, err := service.cockroachDbUtil.BeginTx(ctx, pgx.TxOptions{})
	if err != nil {
		return modelresponses.SetInternalServerErrorResponse()
	}

	defer func() {
		errCommitRollback := service.cockroachDbUtil.CommitOrRollback(tx, ctx, err)
		if errCommitRollback != nil {
			response = modelresponses.SetInternalServerErrorResponse()
		}
	}()

	rowsAffected, err := service.test1Repository.Delete(tx, ctx, deleteRequest.Id)
	if err != nil {
		fmt.Println("err:", deleteRequest.Id, err)
		return modelresponses.SetInternalServerErrorResponse()
	}
	fmt.Println("rowsAffected:", rowsAffected)
	return modelresponses.SetNoContentResponse()
}
