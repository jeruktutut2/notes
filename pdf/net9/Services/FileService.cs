using PdfSharpCore.Drawing;
using PdfSharpCore.Pdf;
using PdfSharpCore.Pdf.IO;
using SixLabors.Fonts;

namespace net9.Services;

public class FileService: IFileService
{
    public async Task<string> GeneratePdf()
    {
        try
        {
            // create new pdf
            string path = "pdfs/merge.pdf";
            var document = new PdfDocument();
            var page = document.AddPage();
            var gpx = XGraphics.FromPdfPage(page);
            gpx.DrawString("Initial Empty PDF", new XFont("Arial", 12), XBrushes.Black, new XRect(0, 0, page.Width, 0)); //page.Height
            document.Save(path);

            // merge pdf
            for (int i = 0; i < 3; i++)
            {
                string partPath = $"pdfs/part{i}.pdf";
                var partDocument = new PdfDocument();
                var partPage = partDocument.AddPage();
                var partGpx = XGraphics.FromPdfPage(partPage);
                partGpx.DrawString(i.ToString(), new XFont("Arial", 12), XBrushes.Black, new XRect(0, 0, page.Width, 0)); //page.Height
                partDocument.Save(partPath);

                // var partInput = PdfReader.Open(partPath, PdfDocumentOpenMode.Import);
            }
            return "success";
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
            return e.ToString();
        }
    }
}