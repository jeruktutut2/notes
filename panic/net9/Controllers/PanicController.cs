using Microsoft.AspNetCore.Mvc;

namespace net.Controllers;

[ApiController]
[Route("api/v1/panic")]
public class PanicContoller: ControllerBase
{
    public PanicContoller()
    {

    }

    [HttpGet]
    public async Task<IActionResult> CheckPanic()
    {
        return Ok();
    }
}