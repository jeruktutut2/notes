namespace net9.Services;

public class FileService: IFileService
{
    private readonly string _filePath = "audios/audio.mp3";
    public async Task<bool> CheckFileExists()
    {
        return File.Exists(_filePath);
    }

    public async Task<(long start, long end, long fileLength, Stream fileStream)> PrepareStream(string rangeHeader)
    {
        var fileStream = new FileStream(_filePath, FileMode.Open, FileAccess.Read, FileShare.Read);
        var fileLength = fileStream.Length;

        long start = 0;
        long end = fileLength - 1;

        if (!string.IsNullOrEmpty(rangeHeader) && rangeHeader.StartsWith("bytes="))
        {
            var ranges = rangeHeader.Replace("bytes=", "").Split("-");
            start = long.Parse(ranges[0]);
            end = ranges.Length > 1 && !string.IsNullOrWhiteSpace(ranges[1]) ? long.Parse(ranges[1]) : end;
        }
        fileStream.Seek(start, SeekOrigin.Begin);
        return (start, end, fileLength, fileStream);
    }

    public async Task Stream(Stream input, Stream output, long contentLength)
    {
        try
        {
            const int bufferSize = 64 * 1024;
            var buffer = new byte[bufferSize];
            long byteHasBeenRead = 0;

            while (byteHasBeenRead < contentLength)
            {
                var toRead = (int)Math.Min(bufferSize, contentLength - byteHasBeenRead);
                var read = await input.ReadAsync(buffer.AsMemory(0, toRead));
                if (read == 0) break;
                await output.WriteAsync(buffer.AsMemory(0, read));
                byteHasBeenRead += read;
            }
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
        }
    }
}