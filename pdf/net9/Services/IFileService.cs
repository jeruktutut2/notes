namespace net9.Services;

public interface IFileService
{
    Task<string> GeneratePdf();
}