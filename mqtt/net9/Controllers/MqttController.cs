using Microsoft.AspNetCore.Mvc;
using net9.Services;

namespace net9.Controllers;

[ApiController]
// [Route("api/v1/mqtt")]
[Route("mqtt")]
public class MqttController: ControllerBase
{
    private readonly IMqttService _mqttService;
    public MqttController(IMqttService mqttService)
    {
        _mqttService = mqttService;
    }

    [HttpGet("send-message/{message}")]
    public async Task<IActionResult> SendMessage([FromRoute] string message)
    {
        var response = await _mqttService.SendMessage(message);
        return StatusCode(200, response);
    }
}