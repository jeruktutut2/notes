using System.Text;
using System.Text.Json;
using System.IO;
// using System.Text;
// using System.Text.Json;
using System.Threading.Tasks;
using System.IO.Pipelines;

namespace net9.Services;

public class StreamService
{
    public class EventData
    {
        public required string Message { get; set; }
    }

    public async Task StreamSSeService(PipeWriter writer) {
        // using var writer = new StreamWriter(responseStream, Encoding.UTF8, leaveOpen: true);
        var options = new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.CamelCase };

        var data1 = JsonSerializer.Serialize(new EventData { Message = "message 1"}) + "\n";
        var bytes1 = Encoding.UTF8.GetBytes(data1);
        await writer.WriteAsync(bytes1);
        await writer.FlushAsync();

        await Task.Delay(2000);

        var data2 = JsonSerializer.Serialize(new EventData { Message = "message 2"}) + "\n";
        var bytes2 = Encoding.UTF8.GetBytes(data2);
        await writer.WriteAsync(bytes2);
        await writer.FlushAsync();

        await Task.Delay(2000);

        var data3 = JsonSerializer.Serialize(new EventData { Message = "message 3"}) + "\n";
        var bytes3 = Encoding.UTF8.GetBytes(data3);
        await writer.WriteAsync(bytes3);
        await writer.FlushAsync();
    }
}