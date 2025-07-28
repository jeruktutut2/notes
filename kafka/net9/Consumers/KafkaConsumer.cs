using Confluent.Kafka;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using System;
using System.Threading;
using System.Threading.Tasks;

namespace net9.Consumers;

public class KafkaConsumer : BackgroundService
{
    private const string BootstrapServers = "localhost:9092";
    private const string Topic = "text-message";
    private const string GroupId = "text-message-consumer-group-table";

    private readonly IConsumer<string, string> _consumer;

    public KafkaConsumer()
    {
        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} kafka: preparing consumer at localhost:9092");
        var config = new ConsumerConfig
        {
            BootstrapServers = BootstrapServers,
            GroupId = GroupId,
            AutoOffsetReset = AutoOffsetReset.Earliest
        };
        _consumer = new ConsumerBuilder<string, string>(config).Build();
    }

    protected override Task ExecuteAsync(CancellationToken stoppingToken)
    {
        return Task.Run(() =>
        {
            _consumer.Subscribe(Topic);
            Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} kafka: subscribed to topic: {Topic}");
            try
            {
                while(!stoppingToken.IsCancellationRequested)
                {
                    try
                    {
                        var consumerResult = _consumer.Consume(stoppingToken);
                        Console.WriteLine($"consumerResult: {consumerResult} {consumerResult.Message.Value}");
                    }
                    catch(ConsumeException e)
                    {
                        Console.WriteLine($"error ConsumeException: {e}");
                    }
                }
            }
            catch(OperationCanceledException e)
            {
                Console.WriteLine($"error OperationCanceledException: {e}");
            }
            finally
            {
                Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} kafka: closing consumer at localhost:9092");
                _consumer.Close();
                Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} kafka: closed consumer at localhost:9092");
            }
        }, stoppingToken);
    }

    public override void Dispose()
    {
        if (_consumer is not null) {
            _consumer.Dispose();
            base.Dispose();
        }
    }
}