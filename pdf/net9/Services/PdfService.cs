using QuestPDF.Fluent;
using QuestPDF.Infrastructure;

namespace net9.Services;

public class PdfService: IPdfService
{
    public byte[] GeneratePdf()
    {
        try
        {
            using var memoryStream = new MemoryStream();
            var document = Document.Create(container =>
            {
                container.Page(page =>
                {
                    page.Margin(50);
                    page.Content().Text("Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.").FontSize(16);
                });
            });
            document.GeneratePdf(memoryStream);
            return memoryStream.ToArray();
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
            return Array.Empty<byte>();
        }
        // return memoryStream.ToArray();
    }
}