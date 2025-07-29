using System.Net.Http.Headers;
using Microsoft.VisualBasic;

namespace net9.Services;

public class FileService: IFileService
{

    public async Task<string> GetFileinfo()
    {
        try
        {
            var filePath = "uploads/file_upload.mp4";
            if (!File.Exists(filePath)) 
            {
                return "0";
            }
            var fileinfo = new FileInfo(filePath);
            var totalSize = fileinfo.Length;
            return totalSize.ToString();
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
            return e.ToString();
        }
    }
    public async Task<string> Download(HttpResponse response, string rangeHeader)
    {
        try
        {
            var filePath = "uploads/file_upload.mp4";
            if (!File.Exists(filePath)) 
            {
                return "cannot find file to download";
            }

            var fileinfo = new FileInfo(filePath);
            var totalSize = fileinfo.Length;

            long start = 0;
            long end = totalSize - 1;
            if (!string.IsNullOrEmpty(rangeHeader) && rangeHeader.StartsWith("bytes="))
            {
                var ranges = rangeHeader.Replace("bytes=", "").Split("-");
                start = long.Parse(ranges[0]);

                if (ranges.Length > 1 && long.TryParse(ranges[1], out var parseEnd))
                {
                    end = parseEnd;
                }
            }

            var length = end - start + 1;
            response.StatusCode = StatusCodes.Status206PartialContent;
            response.Headers.ContentType = "application/octet-stream";
            response.Headers.ContentLength = length;
            response.Headers.ContentRange = $"bytes {start}-{end}/{totalSize}";
            response.Headers.AcceptRanges = "bytes";

            using var fs = new FileStream(filePath, FileMode.Open, FileAccess.Read, FileShare.Read);
            fs.Seek(start, SeekOrigin.Begin);

            byte[] buffer = new byte[64 * 1024];
            int bytesRead;
            long bytesRemaining = length;

            // while ((bytesRead = await fs.ReadAsync(buffer.AsMemory(0, (int)Math.Min(buffer.Length, bytesRemaining)))) > 0 && bytesRemaining > 0)
            while((bytesRead = await fs.ReadAsync(buffer.AsMemory(0, (int)Math.Min(buffer.Length, bytesRemaining)))) > 0 && bytesRemaining > 0)
            {
                await response.Body.WriteAsync(buffer.AsMemory(0, bytesRead));
                bytesRemaining -= bytesRead;
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