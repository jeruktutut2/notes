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

    [HttpGet("stream-video")]
    public async Task<IActionResult> Stream()
    {
        var isFileExists = await _fileService.CheckFileExists();
        if (!isFileExists)
        {
            return StatusCode(404, new { response = "not found" });
        }

        var rangeHeader = Request.Headers.Range.ToString();
        var (start, end, fileLength, fileStream) = await _fileService.PrepareStream(rangeHeader);
        var contentLength = end - start + 1;

        Response.StatusCode = 206;
        Response.ContentType = "video/mp4";
        Response.ContentLength = contentLength;
        Response.Headers.Append("Content-Range", $"bytes {start}-{end}/{fileLength}");
        Response.Headers.Append("Accept-Ranges", "bytes");

        await _fileService.Stream(fileStream, Response.Body, contentLength);
        return new EmptyResult();
    }

}