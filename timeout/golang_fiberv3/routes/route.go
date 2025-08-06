package routes

import (
	"note-golang-fiberv3-timeout/controllers"
	"note-golang-fiberv3-timeout/repositories"
	"note-golang-fiberv3-timeout/services"
	"note-golang-fiberv3-timeout/utils"

	"github.com/gofiber/fiber/v3"
)

func SetTestRoute(app *fiber.App, postgresUtil utils.PostgresUtil) {
	test1Repository := repositories.NewTest1Repository()
	test2Repository := repositories.NewTest2Repository()
	test3Repository := repositories.NewTest3Repository()
	testService := services.NewTestService(postgresUtil, test1Repository, test2Repository, test3Repository)
	testController := controllers.NewTestController(testService)
	app.Post("/test1-with-tx", testController.Test1WithTx)
	app.Post("test1-without-tx", testController.Test1WithoutTx)
}
