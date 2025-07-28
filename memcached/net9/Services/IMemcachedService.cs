namespace net9.Services;

public interface IMemcachedService
{
    Task<string> SetAsync(object value);
    Task<string> GetAsync(string key);

    Task<string> DeleteAsync(string key);
    Task<string> FlushAsync();
}