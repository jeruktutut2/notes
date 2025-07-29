using Microsoft.AspNetCore.Mvc;
using net9.Services;

namespace net9.Controllers;

[ApiController]
// [Route("api/v1/file")]
[Route("file")]
public class FileController: ControllerBase {

    private readonly IFileService _fileService;
    public FileController(IFileService fileService)
    {
        _fileService = fileService;
    }

    [HttpGet("stat")]
    public async Task<IActionResult> GetFileinfo()
    {
        var resp = await _fileService.GetFileinfo();
        return StatusCode(200, new { filename = "file_upload.mp4", size = resp });
    }
    
    [HttpGet("download")]
    public async Task<IActionResult> Download()
    {
        var rangeHeader = Request.Headers.Range.ToString();
        var resp = await _fileService.Download(Response, rangeHeader);
        return StatusCode(200, new { response = resp });
    }

}