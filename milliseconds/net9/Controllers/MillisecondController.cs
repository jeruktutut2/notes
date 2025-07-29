using Microsoft.AspNetCore.Mvc;
using net9.Models.Requests;
using net9.Services;

namespace net9.Controllers;

[ApiController]
// [Route("api/v1/millisecond")]
[Route("millisecond/")]
public class MillisecondController: ControllerBase
{
    private IMillisecondService _millisecondService;
    public MillisecondController(IMillisecondService millisecondService)
    {
        _millisecondService = millisecondService;
    }

    [HttpGet("plus8")]
    public async Task<IActionResult> GetByGMTPlus8([FromBody] MillisecondRequest millisecondRequest)
    {
        var response = await _millisecondService.GetByGMTPlus8(millisecondRequest);
        return StatusCode(200, response);
    }

    [HttpGet("minus8")]
    public async Task<IActionResult> GetByGMTMinus8([FromBody] MillisecondRequest millisecondRequest)
    {
        var response = await _millisecondService.GetByGMTMinus8(millisecondRequest);
        return StatusCode(200, response);
    }
}