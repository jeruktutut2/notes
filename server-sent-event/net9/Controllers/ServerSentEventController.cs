using Microsoft.AspNetCore.Mvc;
using net9.Services;

namespace net9.Controllers;

[ApiController]
[Route("sse")]
public class ServerSentEventController: ControllerBase
{
    private readonly SSEService _sseService;
    public ServerSentEventController(SSEService sseService)
    {
        _sseService = sseService;
    }

    [HttpGet]
    public async Task Subscribe() {
        Response.ContentType = "text/event-stream";
        Response.Headers.CacheControl = "no-cache";

        _sseService.AddClient(Response);

        while (!HttpContext.RequestAborted.IsCancellationRequested)
        {
            await Task.Delay(2000);
        }
    }

    [HttpPost("{message}")]
    public async Task<IActionResult> SendMessage([FromRoute] string message)
    {
        await _sseService.BroadcastMessageAsync(message);
        return StatusCode(200, message);
    }
}