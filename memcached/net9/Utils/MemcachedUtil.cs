using Enyim.Caching;
using Enyim.Caching.Configuration;
using Enyim.Caching.Memcached.Results;
using Microsoft.Extensions.Options;

namespace net9.Utils;

public class MemcachedUtil
{
    private readonly MemcachedClient _client;
    public MemcachedUtil()
    {
        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} memcached: connecting to localhost:11211");
        var loggerFactory = LoggerFactory.Create(builder => builder.AddConsole());
        var options = Options.Create(new MemcachedClientOptions
        {
            Servers = new List<Server>{new Server{Address = "localhost", Port = 11211}}
        });
        var config = new MemcachedClientConfiguration(loggerFactory, options, null, null, null);
        _client = new MemcachedClient(loggerFactory, config);
        Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} memcached: connected to localhost:11211");
    }

    public async Task<bool> SetAsync(string key, object value, TimeSpan expiration)
    {
        return await _client.SetAsync(key, value, expiration);
    }

    public async Task<string?> GetAsync(string key)
    {
        IGetOperationResult<string> result = await _client.GetAsync<string>(key);
        return result.Value;
    }

    public async Task<bool> DeleteAsync(string key)
    {
        return await _client.RemoveAsync(key);
    }

    public async Task FlushAsync()
    {
        await _client.FlushAllAsync();
    }
}