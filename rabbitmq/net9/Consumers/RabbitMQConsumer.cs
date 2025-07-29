
using System.Text;
using net9.Utils;
using RabbitMQ.Client;
using RabbitMQ.Client.Events;

namespace net9.Consumers;

public class RabbitMQConsumer: BackgroundService
{
    private readonly IChannel _channel;
    public RabbitMQConsumer(IChannel channel)
    {
        _channel = channel;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} rabbitmq: waiting for message on: notification");
        var consumer = new AsyncEventingBasicConsumer(_channel);
        consumer.ReceivedAsync += async (model, ea) => {
            var body = ea.Body.ToArray();
            var message = Encoding.UTF8.GetString(body);
            Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} rabbitmq: received message: {message}");
        };
        await _channel.BasicConsumeAsync("notification", autoAck: true, consumer: consumer, cancellationToken: stoppingToken);

        await Task.Delay(Timeout.Infinite, stoppingToken);
    }

    public override async Task StopAsync(CancellationToken cancellationToken)
    {
        if (_channel is not null) {
            await _channel.CloseAsync(cancellationToken: cancellationToken);
            await _channel.DisposeAsync();
        }
        await base.StopAsync(cancellationToken);
    }
}