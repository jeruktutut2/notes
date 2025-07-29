using Microsoft.AspNetCore.Mvc;

namespace net9.Controllers {

    [ApiController]
    [Route("test1")]

    public class Test1Controller: ControllerBase
    {
        public Test1Controller() {
            
        }

        [HttpGet]
        public async Task<IActionResult> GetTest1()
        {
            var requestId = HttpContext.Items["requestId"] as String;
            return Ok(new { requestId = requestId});
        }

        [HttpPost]
        public async Task<IActionResult> PostTest1()
        {
            var requestId = HttpContext.Items["requestId"] as String;
            return Ok(new { requestId = requestId });
        }
    }
}