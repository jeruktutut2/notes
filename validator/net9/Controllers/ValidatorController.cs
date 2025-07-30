using Microsoft.AspNetCore.Mvc;
using net9.Helpers;
using net9.Models.Requests;

namespace net9.Controllers;

[ApiController]
[Route("validator")]
public class ValidatorController: ControllerBase
{
    public ValidatorController()
    {

    }
    
    [HttpPost]
    public async Task<IActionResult> Create([FromBody] CreateRequest createRequest)
    {
        Console.WriteLine("ked dini");
        if (!ModelState.IsValid) {
            Dictionary<String, String> errors = ValidatorHelper.Validate(ModelState, typeof(CreateRequest));
            return StatusCode(400, errors);
        }
        return Ok();
    }
}