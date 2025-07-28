using Microsoft.AspNetCore.Mvc;
using net9.Services;

namespace net9.Controllers;

[ApiController]
// [Route("api/v1/logger")]
[Route("logger")]
public class LoggerController: ControllerBase
{
    private readonly ILoggerService _loggerService;
    public LoggerController(ILoggerService loggerService)
    {
        _loggerService = loggerService;
    }
    
    [HttpGet]
    public IActionResult CheckPanic()
    {
        string response = _loggerService.CheckLogger();
        return StatusCode(200, response);
    }
}