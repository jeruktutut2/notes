package utilmocks

import (
	"context"
	"database/sql"
	"fmt"

	"github.com/jmoiron/sqlx"
	"github.com/stretchr/testify/mock"
)

type PostgresUtilMock struct {
	Mock mock.Mock
}

func (util *PostgresUtilMock) GetDb() *sqlx.DB {
	arguments := util.Mock.Called()
	return arguments.Get(0).(*sqlx.DB)
}

func (util *PostgresUtilMock) BeginTxx(ctx context.Context, options *sql.TxOptions) (*sqlx.Tx, error) {
	arguments := util.Mock.Called(ctx, options)
	return arguments.Get(0).(*sqlx.Tx), arguments.Error(1)
}

func (util *PostgresUtilMock) Close(host string, port string) {
	arguments := util.Mock.Called(host, port)
	fmt.Println(arguments)
}

func (util *PostgresUtilMock) CommitOrRollback(tx *sqlx.Tx, err error) error {
	arguments := util.Mock.Called(tx, err)
	return arguments.Error(0)
}
