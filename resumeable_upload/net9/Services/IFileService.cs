namespace net9.Services;

public interface IFileService
{
    Task<string> Upload(string fileId, string chunkIndex, Stream chunk);
    Task<string> Merge(string fileId, int totalChunks);
    Task<List<int>> CheckFile(string fileId);
    Task<string> UploadAndMerge(string fileId, string chunkIndex, string lastChunkIndex, Stream chunk);
}