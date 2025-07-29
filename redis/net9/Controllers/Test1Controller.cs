using Microsoft.AspNetCore.Mvc;
using net9.Models.Requests;
using net9.Models.Responses;
using net9.Services;

namespace net9.Controllers {

    [ApiController]
    [Route("api/v1/redis")]
    public class Test1Controller: ControllerBase
    {

        private readonly ITest1Service _test1Service;
        public Test1Controller(ITest1Service test1Service) {
            _test1Service = test1Service;
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> Get([FromRoute] string id) {
            Response<GetResponse> response = await _test1Service.Get(id);
            return StatusCode(response.HttpStatusCode, response.BodyResponse);
        }

        [HttpPost]
        public async Task<IActionResult> Create([FromBody] CreateRequest createRequest) {
            Response<CreateResponse> response = await _test1Service.Create(createRequest);
            return StatusCode(response.HttpStatusCode, response.BodyResponse);
        }

        [HttpDelete]
        public async Task<IActionResult> Delete([FromBody] DeleteRequest deleteRequest)
        {
            Response<MessageResponse?> response = await _test1Service.Delete(deleteRequest);
            return StatusCode(response.HttpStatusCode, response.BodyResponse);
        }
    }
}