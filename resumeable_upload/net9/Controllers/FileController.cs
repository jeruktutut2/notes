using Microsoft.AspNetCore.Mvc;
using net9.Services;

namespace net9.Controllers;

[ApiController]
// [Route("api/v1/file")]
[Route("file")]
public class FileController: ControllerBase {

    private IFileService _fileService;
    public FileController(IFileService fileService)
    {
        _fileService = fileService;
    }

    [HttpPost("upload")]
    public async Task<IActionResult> Upload()
    {
        string fileId = Request.Headers["X-File-Id"].ToString();
        string chunkIndex = Request.Headers["X-Chunk-Index"].ToString();
        using var body = Request.Body;
        var response = await _fileService.Upload(fileId, chunkIndex, body);
        return StatusCode(200, response);
    }

    [HttpPost("merge")]
    public async Task<IActionResult> Merge()
    {
        string fileId = Request.Headers["X-File-Id"].ToString();
        if (!int.TryParse(Request.Headers["X-Total-Chunks"], out int totalChunks)) {
            return StatusCode(400, new {response = "cannot convert X-Total-Chunks to int"});
        }
        var response = await _fileService.Merge(fileId, totalChunks);
        return StatusCode(200, response);
    }

    [HttpGet("check-file/{fileId}")]
    public async Task<IActionResult> CheckFile([FromRoute] string fileId)
    {
        var response = await _fileService.CheckFile(fileId);
        return StatusCode(200, new { response = response });
    }

    [HttpPost("upload-merge")]
    public async Task<IActionResult> UploadAndMerge([FromForm] string fileId, [FromForm] string chunkIndex, [FromForm] string lastChunkIndex, [FromForm] IFormFile chunk)
    {
        var response = await _fileService.UploadAndMerge(fileId, chunkIndex, lastChunkIndex, chunk.OpenReadStream());
        return StatusCode(200, new { response = response });
    }
}