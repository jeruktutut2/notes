using Confluent.Kafka;

namespace net9.Services;

public class KafkaService: IKafkaService
{
    private const string BootstrapServers = "localhost:9092";
    private const string Topic = "text-message";

    private readonly IProducer<string, string> _producer;
    public KafkaService()
    {
        var config = new ProducerConfig
        {
            BootstrapServers = BootstrapServers
        };

        _producer = new ProducerBuilder<string, string>(config).Build();
    }

    public async Task<string> SendMessage(string message) {
        var deliveryResult = await _producer.ProduceAsync(Topic, new Message<string, string>{
            Key = Guid.NewGuid().ToString(),
            Value = message
        });
        return "ok";
    }
}