package initialize

import "github.com/sirupsen/logrus"

type defaultFieldHook struct {
}

func (hook *defaultFieldHook) Levels() []logrus.Level {
	return logrus.AllLevels
}

func (hook *defaultFieldHook) Fire(entry *logrus.Entry) error {
	entry.Data["app"] = "app-backend"
	return nil
}

func NewLogger() *logrus.Logger {
	logger := logrus.New()
	logger.SetFormatter(&logrus.JSONFormatter{})
	logger.SetLevel(logrus.WarnLevel)
	logger.AddHook(&defaultFieldHook{})
	return logger
}
