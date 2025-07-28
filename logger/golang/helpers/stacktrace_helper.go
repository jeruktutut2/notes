package helpers

import (
	"runtime/debug"
	"strings"
)

func GetStacktrace() string {
	stacktrace := string(debug.Stack())
	stacktrace = strings.ReplaceAll(stacktrace, "\n", "")
	return stacktrace
}
