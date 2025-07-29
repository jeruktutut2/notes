using System.Text;
using net9.Utils;
using RabbitMQ.Client;

namespace net9.Services;

public class Test1Servive: ITest1Service
{
    private readonly IChannel _channel;
    public Test1Servive(IChannel channel)
    {
        _channel = channel;
    }

    public async Task<string> SendMessage(string message) {
        var body = Encoding.UTF8.GetBytes(message);
        await _channel.BasicPublishAsync(exchange: string.Empty, routingKey: "notification", body: body);
        return "ok";
    }
}