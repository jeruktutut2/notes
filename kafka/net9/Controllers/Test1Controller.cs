using Microsoft.AspNetCore.Mvc;
using net9.Services;

namespace net9.Controllers {

    [ApiController]
    // [Route("api/v1/message")]
    [Route("kafka")]
    public class Test1Controller: ControllerBase
    {
        private readonly IKafkaService _kafkaService;
        public Test1Controller(IKafkaService kafkaService) {
            _kafkaService = kafkaService;
        }

        [HttpGet("send-message/{message}")]
        public async Task<IActionResult> SendMessage([FromRoute] string message) {
            var response = await _kafkaService.SendMessage(message);
            return StatusCode(200, response);
        }
    }
}