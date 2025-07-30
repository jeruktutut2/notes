using System.Collections.Concurrent;
using System.Net.WebSockets;
using System.Text;

namespace net9.Services;

public class ChatWebSocketManager
{
    private readonly ConcurrentDictionary<string, WebSocket> _clients = new();

    public void AddClient(string clientId, WebSocket webSocket)
    {
        _clients[clientId] = webSocket;
    }

    public async Task RemoveClient(string clientId)
    {
        if (_clients.TryRemove(clientId, out var webSocket))
        {
            await webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "client disconnected", CancellationToken.None);
        }
    }

    public async Task SendMessageAsync(string clientId, string message)
    {
        if (_clients.TryGetValue(clientId, out var webSocket) && webSocket.State == WebSocketState.Open)
        {
            var buffer = Encoding.UTF8.GetBytes(message);
            await webSocket.SendAsync(buffer, WebSocketMessageType.Text, true, CancellationToken.None);
        }
    }
}