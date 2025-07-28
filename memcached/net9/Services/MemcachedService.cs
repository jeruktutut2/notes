using net9.Utils;

namespace net9.Services;

public class MemcachedService: IMemcachedService
{
    private readonly MemcachedUtil _memcachedUtil;

    public MemcachedService(MemcachedUtil memcachedUtil)
    {
        _memcachedUtil = memcachedUtil;
    }
    public async Task<string> SetAsync(object value) {
        // TimeSpan.FromMinutes(5)
        var key = Guid.NewGuid().ToString();
        bool isSet = await _memcachedUtil.SetAsync(key, value, TimeSpan.Zero);
        Console.WriteLine($"isSet: {isSet}, key: {key}, value: {value}");
        return key;
    }

    public async Task<string> GetAsync(string key)
    {
        string? getValue = await _memcachedUtil.GetAsync(key);
        Console.WriteLine($"getValue: key: {key}, value: {getValue}");
        return "ok";
    }

    public async Task<string> DeleteAsync(string key)
    {
        bool isDeleted = await _memcachedUtil.DeleteAsync(key);
        Console.WriteLine($"isDeleted: {isDeleted}");
        return "ok";
    }

    public async Task<string> FlushAsync()
    {
        await _memcachedUtil.FlushAsync();
        return "ok";
    }
}