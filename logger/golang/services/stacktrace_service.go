package services

import (
	"context"
	"errors"

	"note-golang-logger/helpers"

	"github.com/sirupsen/logrus"
)

type LoggerService interface {
	CheckLogger(ctx context.Context) string
}

type loggerService struct {
	logger *logrus.Logger
}

func NewLoggerService(logger *logrus.Logger) LoggerService {
	return &loggerService{
		logger: logger,
	}
}

func (service *loggerService) CheckLogger(ctx context.Context) string {
	service.logger.Trace("logger trace")
	service.logger.Debug("logger debug")
	service.logger.Info("logger info")
	service.logger.Warn("logger warn")
	err := errors.New("this is error")
	service.logger.WithError(err).WithField("requestId", "requestId").WithField("stacktrace", helpers.GetStacktrace()).Error("this error message")
	return "ok"
}
