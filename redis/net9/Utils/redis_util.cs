using StackExchange.Redis;

namespace net9.Utils;

public class RedisUtil {
    private readonly IConnectionMultiplexer _connection;
    private readonly IDatabase _db;

    public RedisUtil(IConfiguration configuration) {
        string connectionString = configuration.GetValue<string>("Redis:ConnectionString");
        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} redis: connecting to {connectionString}");
        _connection = ConnectionMultiplexer.Connect(connectionString);
        int dbIndex = configuration.GetValue<int>("Redis:Database");
        _db = _connection.GetDatabase(dbIndex);
        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} redis: connected to {connectionString}");
    }

    public IDatabase GetDatabase() => _db;
}