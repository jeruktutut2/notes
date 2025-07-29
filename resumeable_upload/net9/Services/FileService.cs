using System.Text.RegularExpressions;
using net9.Helpers;

namespace net9.Services;

public class FileService: IFileService
{
    private readonly string _uploadsDir;

    public FileService(IWebHostEnvironment env)
    {
        _uploadsDir = Path.Combine(env.ContentRootPath, "uploads");
    }
    public async Task<string> Upload(string fileId, string chunkIndex, Stream chunk)
    {
        try
        {
            var chunkPath = Path.Combine(_uploadsDir, $"{fileId}.part{chunkIndex}");
            using (var stream = new FileStream(chunkPath, FileMode.Create)) {
                await chunk.CopyToAsync(stream);
            }
            return "success";
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
            return e.ToString();
        }
    }

    public async Task<string> Merge(string fileId, int totalChunks)
    {
        try
        {
            var mergeFilePath = Path.Combine(_uploadsDir, $"{fileId}.merged");
            using (var mergeFileStream = new FileStream(mergeFilePath, FileMode.Create))
            {
                for (int i = 0; i < totalChunks; i++)
                {
                    var partFilePath = Path.Combine(_uploadsDir, $"{fileId}.part{i}");
                    using var partFileStream = new FileStream(partFilePath, FileMode.Open);
                    await partFileStream.CopyToAsync(mergeFileStream);
                    if (System.IO.File.Exists(partFilePath))
                    {
                        System.IO.File.Delete(partFilePath);
                    }
                }
            }

            var mergeStream = new FileStream(mergeFilePath, FileMode.Open);
            var extention = FileHelper.DetectFileExtensionFromStream(mergeStream);
            mergeStream.Close();
            var newMergePath = Path.ChangeExtension(mergeFilePath, extention);
            System.IO.File.Move(mergeFilePath, newMergePath);
            return "success";
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
            return e.ToString();
        }
    }

    public async Task<List<int>> CheckFile(string fileId)
    {
        var result = new List<int>();
        try
        {
            var files = Directory.GetFiles(_uploadsDir, $"{fileId}.part*");
            foreach(var file in files)
            {
                var fileName = Path.GetFileName(file);
                var match = Regex.Match(fileName, @"\.part(\d+)$");
                if (match.Success && int.TryParse(match.Groups[1].Value, out int index))
                {
                    result.Add(index);
                }
            }
            result.Sort();
            return result;
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
            return result;
        }
    }

    public async Task<string> UploadAndMerge(string fileId, string chunkIndex, string lastChunkIndex, Stream chunk)
    {
        try
        {
            var mergeFilePath = $"{_uploadsDir}/{fileId}.merged";
            using var mergeFileStream = new FileStream(mergeFilePath, FileMode.OpenOrCreate, FileAccess.Write);
            mergeFileStream.Seek(0, SeekOrigin.End);
            await chunk.CopyToAsync(mergeFileStream);
            Thread.Sleep(1000);
            if (chunkIndex == lastChunkIndex)
            {
                var mergeStream = new FileStream(mergeFilePath, FileMode.Open);
                var extention = FileHelper.DetectFileExtensionFromStream(mergeStream);
                Console.WriteLine($"extention: {extention}");
                mergeStream.Close();
                var newMergePath = Path.ChangeExtension(mergeFilePath, extention);
                System.IO.File.Move(mergeFilePath, newMergePath);
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