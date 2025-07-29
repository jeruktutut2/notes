using System.Text.Json;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Text;
using System.Threading.Tasks;
using net9.Services;

namespace net9.Controllers;

[ApiController]
[Route("stream")]
public class StreamController: ControllerBase
{
    private readonly StreamService _streamService;
    public StreamController(StreamService streamService)
    {
        _streamService = streamService;
    }
    
    public class EventData
    {
        public required string Message { get; set; }
    }

    [HttpGet("json-stream")]
    public async IAsyncEnumerable<EventData> GetEvents()
    {
        yield return new EventData { Message = "message 1"};
        await Task.Delay(2000);
        yield return new EventData { Message = "message 2"};
        await Task.Delay(2000);
        yield return new EventData { Message = "message 3"};
    }

    [HttpGet("sse")]
    public async Task GetSSE()
    {
        Response.ContentType = "text/event-stream";
        Response.Headers.CacheControl = "no-cache";
        Response.Headers.Connection = "keep-alive";

        var data1 = JsonSerializer.Serialize(new EventData { Message = "message 1"}) + "\n\n";
        var bytes1 = Encoding.UTF8.GetBytes(data1);
        await Response.BodyWriter.WriteAsync(bytes1);
        await Response.BodyWriter.FlushAsync();

        await Task.Delay(2000);

        var data2 = JsonSerializer.Serialize(new EventData { Message = "message 1"}) + "\n\n";
        var bytes2 = Encoding.UTF8.GetBytes(data2);
        await Response.BodyWriter.WriteAsync(bytes2);
        await Response.BodyWriter.FlushAsync();

        await Task.Delay(2000);

        var data3 = JsonSerializer.Serialize(new EventData { Message = "message 1"}) + "\n\n";
        var bytes3 = Encoding.UTF8.GetBytes(data3);
        await Response.BodyWriter.WriteAsync(bytes3);
        await Response.BodyWriter.FlushAsync();
    }

    [HttpGet("sse-service")]
    public async Task StreamSSe() {
        Response.ContentType = "application/json";
        Response.Headers.CacheControl = "no-cache";
        Response.Headers.Connection = "keep-alive";
        await _streamService.StreamSSeService(Response.BodyWriter);
    }
}