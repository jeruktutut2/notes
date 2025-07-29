using Microsoft.AspNetCore.Mvc;
using net9.Services;

namespace net9.Controllers {

    [ApiController]
    // [Route("api/v1/message")]
    [Route("rabbitmq")]
    public class Test1Controller: ControllerBase
    {
        private readonly ITest1Service _test1Service;
        public Test1Controller(ITest1Service test1Service) {
            _test1Service = test1Service;
        }

        [HttpGet("send-message/{message}")]
        public async Task<IActionResult> SendMessage([FromRoute] string message) {
            string response = await _test1Service.SendMessage(message);
            return StatusCode(200, response);
        }
    }
}