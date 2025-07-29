using MQTTnet;
using MQTTnet.Protocol;

namespace net9.Publisher;

public class MqttPublisher
{
    private readonly IMqttClient _mqttClient;
    private readonly MqttClientOptions _options;
    public MqttPublisher()
    {
        var factory = new MqttClientFactory();
        _mqttClient =  factory.CreateMqttClient();

        _options = new MqttClientOptionsBuilder()
            .WithTcpServer("localhost", 1883)
            .WithClientId("publisher")
            .Build();
        
        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} mqtt publisher: connecting to localhost:1883");
        Task.Run(async () => await _mqttClient.ConnectAsync(_options));
        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} mqtt publisher: connected to localhost:1883");
    }
    
    public async Task PublisAsync(string message)
    {   
        var mqttMessage = new MqttApplicationMessageBuilder()
            .WithTopic("test/topic")
            .WithPayload(message)
            .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.AtLeastOnce)
            .Build();
        await _mqttClient.PublishAsync(mqttMessage);
        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} send message: {message}");
    }

    public async ValueTask DisposeAsync()
    {
        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} mqtt: disconnecting to localhost:1883");
        if (_mqttClient.IsConnected)
        {
            await _mqttClient.DisconnectAsync();
        }
        _mqttClient.Dispose();
        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} mqtt: disconnected to localhost:1883");
    }
}