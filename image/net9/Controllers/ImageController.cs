using Microsoft.AspNetCore.Mvc;
using net9.Models.Requests;
using net9.Services;

namespace net9.Controllers;

[ApiController]
// [Route("api/v1/image")]
[Route("image")]
public class ImageController: ControllerBase
{
    private readonly IImageService _imageservice;
    public ImageController(IImageService imageService)
    {
        _imageservice = imageService;
    }
    
    [HttpPost]
    public IActionResult CheckImage([FromBody] ImageRequest imageRequest)
    {
        string response = _imageservice.CheckImage(imageRequest);
        return StatusCode(200, response);
    }
}