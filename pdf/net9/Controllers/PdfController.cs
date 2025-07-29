using Microsoft.AspNetCore.Mvc;
using net9.Services;

namespace net9.Controllers;

[ApiController]
// [Route("api/v1/pdf")]
[Route("pdf")]
public class PdfController: ControllerBase
{
    private IPdfService _pdfService;
    public PdfController(IPdfService pdfService)
    {
        _pdfService = pdfService;
    }
    
    [HttpGet]
    public IActionResult GeneratePdf()
    {
        var pdfBytes = _pdfService.GeneratePdf();
        return File(pdfBytes, "application/pdf", "generated.pdf");
    }
}