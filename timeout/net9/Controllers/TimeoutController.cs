using Microsoft.AspNetCore.Mvc;
using net9.Services;

namespace net9.Controllers;

[ApiController]
[Route("timeout")]
public class TimeoutController : ControllerBase
{
    private readonly ITimeoutService _timeoutService;
    public TimeoutController(ITimeoutService timeoutService)
    {
        _timeoutService = timeoutService;
    }

    [HttpGet("without-tx")]
    public async Task<IActionResult> TimeoutWithoutTx()
    {
        var cancellationToken = HttpContext.Items["RequestTimeoutToken"] as CancellationToken? ?? HttpContext.RequestAborted;
        var response = await _timeoutService.TimeoutWithoutTx(cancellationToken);
        return Ok(response);
    }

    [HttpGet("with-tx")]
    public async Task<IActionResult> TimeoutWithTx()
    {
        var cancellationToken = HttpContext.Items["RequestTimeoutToken"] as CancellationToken? ?? HttpContext.RequestAborted;
        var response = await _timeoutService.TimeoutWithTx(cancellationToken);
        return Ok(response);
    }
    
    [HttpGet("change-timeout")]
    public async Task<IActionResult> ChangeTimeout()
    {
        var cancellationToken = HttpContext.Items["RequestTimeoutToken"] as CancellationToken? ?? HttpContext.RequestAborted;
        using var timeoutCts = CancellationTokenSource.CreateLinkedTokenSource(cancellationToken);
        timeoutCts.CancelAfter(TimeSpan.FromSeconds(3));
        var response = await _timeoutService.TimeoutWithTx(timeoutCts.Token);
        return Ok(response);
    }
}