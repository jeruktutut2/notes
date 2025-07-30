package routes

import (
	"note-golang-fiber-timeout/controllers"
	"note-golang-fiber-timeout/repositories"
	"note-golang-fiber-timeout/services"
	"note-golang-fiber-timeout/utils"

	"github.com/gofiber/fiber/v2"
)

func SetRoute(app *fiber.App, postgresUtil utils.PostgresUtil) {
	test1Repository := repositories.NewTest1Repository()
	test2Repository := repositories.NewTest2Repository()
	test3Repository := repositories.NewTest3Repository()
	testService := services.NewTestService(postgresUtil, test1Repository, test2Repository, test3Repository)
	testController := controllers.NewTestController(testService)
	app.Get("/timeout/with-tx", testController.Test1WithTx)
	app.Post("/timeout/without-tx", testController.Test1WithoutTx)
	app.Get("/timeout/context-done", testController.Test1TxDone)
}
