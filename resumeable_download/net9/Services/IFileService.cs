namespace net9.Services;

public interface IFileService
{
    Task<string> GetFileinfo();
    Task<string> Download(HttpResponse response, string rangeHeader);
}