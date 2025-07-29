using Microsoft.AspNetCore.Mvc;
using net9.Services;

namespace net9.Controllers;

[ApiController]
[Route("file")]
public class FileController: ControllerBase
{
    private readonly IFileService _fileService;
    public FileController(IFileService fileService)
    {
        _fileService = fileService;
    }

    [HttpGet("show-pdf")]
    public async Task<IActionResult> GeneratePdf()
    {
        // var pdfBytes = _pdfService.GeneratePdf();
        // return File(pdfBytes, "application/pdf", "generated.pdf");
        var response = await _fileService.GeneratePdf();
        return StatusCode(200, new {response = response});
    }

}