using RabbitMQ.Client;
using RabbitMQ.Client.Events;


namespace net9.Utils;

public class RabbitMQUtil: IAsyncDisposable
{
    private readonly IConnectionFactory _connectionFactory;
    private IConnection _connection;
    private IChannel _channel;

    public RabbitMQUtil()
    {
        _connectionFactory = new ConnectionFactory()
        {
            HostName = "localhost",
            UserName = "user",
            Password = "password",
            Port = 5672
        };
    }

    public async Task InitializeAsync()
    {
        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} rabbitmq: connecting to localhost:5672");
        _connection = await _connectionFactory.CreateConnectionAsync();
        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} rabbitmq: connected to localhost:5672");

        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} rabbitmq: creating channel");
        _channel = await _connection.CreateChannelAsync();
        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} rabbitmq: created channel");

        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} rabbitmq: creating queue: notification");
        await _channel.QueueDeclareAsync(queue: "notification", durable: false, exclusive: false, autoDelete: false, arguments: null);
        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} rabbitmq: creating queue: notification");
    }

    public IChannel GetChannel() => _channel ?? throw new InvalidOperationException("Channel not initialized");
    
    public async ValueTask DisposeAsync()
    {
        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} rabbitmq: closing to localhost:5672");
        await _connection.CloseAsync();
        await _connection.DisposeAsync();
        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} rabbitmq: closed to localhost:5672");
    }
}