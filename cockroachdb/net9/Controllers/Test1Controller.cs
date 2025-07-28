using Microsoft.AspNetCore.Mvc;
using net9.Models.Requests;
using net9.Services;

namespace net9.Controllers;

[ApiController]
// [Route("api/v1/millisecond")]
[Route("test1")]
public class Test1Controller: ControllerBase {

    private ITest1Service _test1Service;
    public Test1Controller(ITest1Service test1Service)
    {
        _test1Service = test1Service;
    }

    [HttpPost]
    public async Task<IActionResult> Create([FromBody] CreateRequest createRequest)
    {
        var response = await _test1Service.Create(createRequest);
        return StatusCode(response.HttpStatuscode, response.BodyResponse);
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetById([FromRoute] string id)
    {
        var isUuidValid = Guid.TryParse(id, out Guid uuidv7);
        if (!isUuidValid) {
            return StatusCode(400, new { response = "not an uuid v7"});
        }
        var response = await _test1Service.GetById(uuidv7);
        return StatusCode(response.HttpStatuscode, response.BodyResponse);
    }

    [HttpGet]
    public async Task<IActionResult> GetAll()
    {
        var response = await _test1Service.GetAll();
        return StatusCode(response.HttpStatuscode, response.BodyResponse);
    }

    [HttpPut]
    public async Task<IActionResult> Update([FromBody] UpdateRequest updateRequest)
    {
        var response = await _test1Service.Update(updateRequest);
        return StatusCode(response.HttpStatuscode, response.BodyResponse);
    }

    [HttpDelete]
    public async Task<IActionResult> Delete([FromBody] DeleteRequest deleteRequest)
    {
        var response = await _test1Service.Delete(deleteRequest);
        return StatusCode(response.HttpStatuscode, response.BodyResponse);
    }
}