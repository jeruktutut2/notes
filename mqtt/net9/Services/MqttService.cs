using net9.Publisher;

namespace net9.Services;

public class MqttService: IMqttService
{
    private readonly MqttPublisher _mqttPublisher;
    public MqttService(MqttPublisher mqttPublisher)
    {
        _mqttPublisher = mqttPublisher;
    }

    public async Task<string> SendMessage(string message) {
        await _mqttPublisher.PublisAsync(message);
        return "ok";
    }
}