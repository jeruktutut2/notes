using net9.Models.Requests;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.Formats;

namespace net9.Services;

public class ImageService: IImageService
{
    public string CheckImage(ImageRequest imageRequest)
    {
        try
        {
            byte[] imageBytes = Convert.FromBase64String(imageRequest.ImageBase64);
            var validSignatures = new List<byte[]>
            {
                new byte[] { 0xFF, 0xD8, 0xFF },       // JPEG
                new byte[] { 0x89, 0x50, 0x4E, 0x47 }, // PNG
                new byte[] { 0x47, 0x49, 0x46, 0x38 }, // GIF
                new byte[] { 0x52, 0x49, 0x46, 0x46 }  // WEBP
            };
            bool isValidMagicBytes = validSignatures.Any(sig => imageBytes.Take(sig.Length).SequenceEqual(sig));
            if (!isValidMagicBytes) return "false";
            using var stream = new MemoryStream(imageBytes);
            using var image = Image.LoadAsync(stream);
            return "ok";
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
            return "error";
        }
    }
}