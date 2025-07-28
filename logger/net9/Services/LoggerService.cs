using Microsoft.Extensions.Logging;

namespace net9.Services;

public class LoggerService: ILoggerService
{
    private readonly ILogger<LoggerService> _logger;

    public LoggerService(ILogger<LoggerService> logger)
    {
        _logger = logger;
    }

    public string CheckLogger()
    {
        _logger.LogCritical("Ini log Critical {T}", "test1");
        return "ok";
    }
}