package services

import (
	"context"
	"database/sql"
	"fmt"
	modelentities "timeout/models/entities"
	"timeout/repositories"
	"timeout/utils"
)

type TestService interface {
	TestWithTx(ctx context.Context) (result string)
	TestWithoutTx(ctx context.Context) (result string)
}

type testService struct {
	PostgresUtil    utils.PostgresUtil
	Test1Repository repositories.Test1Repository
	Test2Repository repositories.Test2Repository
	Test3Repository repositories.Test3Repository
}

func NewTestService(postgresUtil utils.PostgresUtil, test1Repository repositories.Test1Repository, test2Repository repositories.Test2Repository, test3Repository repositories.Test3Repository) TestService {
	return &testService{
		PostgresUtil:    postgresUtil,
		Test1Repository: test1Repository,
		Test2Repository: test2Repository,
		Test3Repository: test3Repository,
	}
}

func (service *testService) TestWithTx(ctx context.Context) (result string) {
	tx, err := service.PostgresUtil.BeginTxx(ctx, &sql.TxOptions{})
	if err != nil {
		return ""
	}
	defer func() {
		errCommitOrRollback := service.PostgresUtil.CommitOrRollback(tx, err)
		if errCommitOrRollback != nil {
			result = ""
		}
	}()

	var test1 modelentities.Test1
	test1.Test = "test 1"
	rowsAffected, err := service.Test1Repository.Create(tx, ctx, test1)
	if err != nil {
		fmt.Println("error when create test 1:", err)
		result = ""
		return
	}
	fmt.Println("create test 1:", rowsAffected)

	sleep1, err := service.Test1Repository.Sleep(tx, ctx, 3)
	if err != nil {
		fmt.Println("error when sleep 1:", err)
		result = sleep1
		return
	}
	fmt.Println("sleep1:", sleep1)

	var test2 modelentities.Test2
	test2.Test = "test 2"
	rowsAffected, err = service.Test2Repository.Create(tx, ctx, test2)
	if err != nil {
		fmt.Println("error when create 2:", err)
		result = ""
		return
	}
	fmt.Println("create test 2:", rowsAffected)

	sleep2, err := service.Test2Repository.Sleep(tx, ctx, 3)
	if err != nil {
		result = sleep2
		fmt.Println("error when sleep 2:", err)
		return
	}
	fmt.Println("sleep2:", sleep2)

	var test3 modelentities.Test3
	test3.Test = "test 3"
	rowsAffected, err = service.Test3Repository.Create(tx, ctx, test3)
	if err != nil {
		result = ""
		fmt.Println("error when create 3:", err)
		return
	}
	fmt.Println("create test 3:", rowsAffected)

	sleep3, err := service.Test3Repository.Sleep(tx, ctx, 3)
	if err != nil {
		result = ""
		fmt.Println("error when sleep3:", err)
		return
	}
	fmt.Println("sleep3:", sleep3)

	return "mantap"
}

func (service *testService) TestWithoutTx(ctx context.Context) (result string) {
	var test1 modelentities.Test1
	test1.Test = "test 1"
	rowsAffected, err := service.Test1Repository.CreateWithDb(service.PostgresUtil.GetDb(), ctx, test1)
	if err != nil {
		fmt.Println("error when create test 1:", err)
		result = ""
		return
	}
	fmt.Println("create test 1:", rowsAffected)

	sleep1, err := service.Test1Repository.SleepWithDb(service.PostgresUtil.GetDb(), ctx, 3)
	if err != nil {
		fmt.Println("error when sleep 1:", err)
		result = sleep1
		return
	}
	fmt.Println("sleep1:", sleep1)

	var test2 modelentities.Test2
	test2.Test = "test 2"
	rowsAffected, err = service.Test2Repository.CreateWithDb(service.PostgresUtil.GetDb(), ctx, test2)
	if err != nil {
		fmt.Println("error when create 2:", err)
		result = ""
		return
	}
	fmt.Println("create test 2:", rowsAffected)

	sleep2, err := service.Test2Repository.SleepWithDb(service.PostgresUtil.GetDb(), ctx, 3)
	if err != nil {
		result = sleep2
		fmt.Println("error when sleep 2:", err)
		return
	}
	fmt.Println("sleep2:", sleep2)

	var test3 modelentities.Test3
	test3.Test = "test 3"
	rowsAffected, err = service.Test3Repository.CreateWithDb(service.PostgresUtil.GetDb(), ctx, test3)
	if err != nil {
		result = ""
		fmt.Println("error when create 3:", err)
		return
	}
	fmt.Println("create test 3:", rowsAffected)

	sleep3, err := service.Test3Repository.SleepWithDb(service.PostgresUtil.GetDb(), ctx, 3)
	if err != nil {
		result = ""
		fmt.Println("error when sleep3:", err)
		return
	}
	fmt.Println("sleep3:", sleep3)

	return "mantap"
}
