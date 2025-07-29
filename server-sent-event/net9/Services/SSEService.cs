using System.Collections.Concurrent;
using System.Text;

namespace net9.Services;

public class SSEService
{
    private readonly ConcurrentBag<HttpResponse> _clients = new();

    public void AddClient(HttpResponse httpResponse) {
        _clients.Add(httpResponse);
    }

    public async Task BroadcastMessageAsync(string message) {
         var bytes = Encoding.UTF8.GetBytes(message + "\n");

         foreach(var client in _clients) {
            try
            {
                await client.BodyWriter.WriteAsync(bytes);
                await client.BodyWriter.FlushAsync();
            }
            catch(Exception e)
            {
                Console.WriteLine($"error: {e}");
            }
         }
    }
}