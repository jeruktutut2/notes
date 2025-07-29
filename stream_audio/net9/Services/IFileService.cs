namespace net9.Services;

public interface IFileService
{
    Task<bool> CheckFileExists();
    Task<(long start, long end, long fileLength, Stream fileStream)> PrepareStream(string rangeHeader);
    Task Stream(Stream input, Stream output, long contentLength);
}