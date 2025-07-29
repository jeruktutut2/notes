using Microsoft.AspNetCore.Mvc;
using net9.Models.Requests;
using net9.Services;

namespace net9.Controllers {

    [ApiController]
    [Route("rsa")]
    public class RsaController : ControllerBase
    {
        private readonly IRsaService _rsaService;
        public RsaController(IRsaService rsaService)
        {
            _rsaService = rsaService;
        }

        [HttpGet("sign")]
        public async Task<IActionResult> Sign([FromBody] SignRequest signRequest)
        {
            // var requestId = HttpContext.Items["requestId"] as String;
            // return Ok(new { requestId = requestId});
            var response = _rsaService.Sign(signRequest);
            return StatusCode(200, response);
        }

        [HttpGet("verify")]
        public async Task<IActionResult> Verify([FromBody] VerifyRequest verifyRequest)
        {
            var response = _rsaService.Verify(verifyRequest);
            return StatusCode(200, response);
        }
    }
}