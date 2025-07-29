using Microsoft.AspNetCore.Mvc;
using net9.Models.Requests;
using net9.Services;

namespace net9.Controllers {

    [ApiController]
    [Route("api/v1/test1")]
    public class Test1Controller(ITest1Service test1Service) : ControllerBase
    {
        private readonly ITest1Service _test1Service = test1Service;

        [HttpGet("{id}")]
        public async Task<IActionResult> GetTest1([FromRoute] int id)
        {
            var response = await _test1Service.GetById(id);
            return StatusCode(response.HttpStatuscode, response.BodyResponse);
        }

        [HttpPost]
        public async Task<IActionResult> PostTest1([FromBody] Test1CreateRequest test1CreateRequest)
        {
            var response = await _test1Service.Create(test1CreateRequest);
            return StatusCode(response.HttpStatuscode, response.BodyResponse);
        }

        [HttpPut]
        public async Task<IActionResult> UpdateTest1([FromBody] Test1UpdateRequest test1UpdateRequest)
        {
            var response = await _test1Service.Update(test1UpdateRequest);
            return StatusCode(response.HttpStatuscode, response.BodyResponse);
        }

        [HttpDelete]
        public async Task<IActionResult> DeleteTest1([FromBody] Test1DeleteRequest test1DeleteRequest)
        {
            var response = await _test1Service.Delete(test1DeleteRequest);
            return StatusCode(response.HttpStatuscode, response.BodyResponse);
        }
    }
}