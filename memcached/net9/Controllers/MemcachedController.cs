using Microsoft.AspNetCore.Mvc;
using net9.Models.Requests;
using net9.Services;

namespace net9.Controllers;

[ApiController]
// [Route("api/v1/test1")]
[Route("memcached")]
public class MemcachedController: ControllerBase
{
    private readonly IMemcachedService _memcachedService;
    public MemcachedController(IMemcachedService memcachedService)
    {
        _memcachedService = memcachedService;
    }
    
    [HttpPost]
    public async Task<IActionResult> SetAsync([FromBody] CreateRequest createRequest)
    {
        var response = await _memcachedService.SetAsync(createRequest.Message);
        return StatusCode(200, response);
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetAsync([FromRoute] string id)
    {
        var response = await _memcachedService.GetAsync(id);
        return StatusCode(200, response);
    }

    [HttpDelete]
    public async Task<IActionResult> DeleteAsync([FromBody] DeleteRequest deleteRequest)
    {
        var response = await _memcachedService.DeleteAsync(deleteRequest.Id);
        return StatusCode(200, response);
    }

    [HttpPost("flush")]
    public async Task<IActionResult> Flush()
    {
        var response = await _memcachedService.FlushAsync();
        return StatusCode(200, response);
    }
}