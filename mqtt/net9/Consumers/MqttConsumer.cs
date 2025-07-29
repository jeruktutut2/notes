using System.Text;
using MQTTnet;

namespace net9.Consumers;

public class MqttConsumer: BackgroundService
{
    private readonly IMqttClient _mqttClient;
    public MqttConsumer()
    {
        var factory = new MqttClientFactory();
        _mqttClient =  factory.CreateMqttClient();
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        var options = new MqttClientOptionsBuilder()
            .WithTcpServer("localhost", 1883)
            .WithClientId("subscriber")
            .Build();
        
        _mqttClient.ApplicationMessageReceivedAsync += e =>
        {
            var payload = Encoding.UTF8.GetString(e.ApplicationMessage.Payload);
            Console.WriteLine($"received message: {payload}");
            return Task.CompletedTask;
        };

        await _mqttClient.ConnectAsync(options, stoppingToken);
        await _mqttClient.SubscribeAsync("test/topic", cancellationToken: stoppingToken);

        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} Subscribed to topic: test/topic");
        await Task.Delay(Timeout.Infinite, stoppingToken);
    }
}