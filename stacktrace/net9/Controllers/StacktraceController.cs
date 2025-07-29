using Microsoft.AspNetCore.Mvc;
using net9.Services;

namespace net9.Controllers;

[ApiController]
// [Route("api/v1/stacktrace")]
[Route("stacktrace")]
public class StacktraceController: ControllerBase
{
    private readonly IStacktraceService _stacktraceService;
    public StacktraceController(IStacktraceService stacktraceService)
    {
        _stacktraceService = stacktraceService;
    }

    [HttpGet("environtment-stacktrace")]
    public async Task<IActionResult> EnvirontmentStacktrace()
    {
        string stacktrace = _stacktraceService.EnvirontmentStacktrace();
        return Ok();
    }

    [HttpGet("exception-stacktrace")]
    public async Task<IActionResult> ExceptionStacktrace()
    {
        string stacktrace = _stacktraceService.ExceptionStacktrace();
        return Ok();
    }

    [HttpGet("print-stacktrace")]
    public async Task<IActionResult> PrintStacktrace()
    {
        string stacktrace = _stacktraceService.PrintStacktrace();
        return Ok();
    }
}