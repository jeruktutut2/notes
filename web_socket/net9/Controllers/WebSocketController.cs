using System.Net.WebSockets;
using System.Text;
using Microsoft.AspNetCore.Mvc;
using net9.Services;

namespace net9.Controllers;

[ApiController]
// [Route("api/v1/web-socket")]
[Route("ws/chat")]
public class WebSocketController: ControllerBase
{
    private readonly ChatWebSocketManager _chatWebSocketManager;
    public WebSocketController(ChatWebSocketManager chatWebSocketManager)
    {
        _chatWebSocketManager = chatWebSocketManager;
    }
    
    [HttpGet("connect/{clientId}")]
    public async Task<IActionResult> Connect([FromRoute] string clientId)
    {
        if (HttpContext.WebSockets.IsWebSocketRequest)
        {
            using var webSocket = await HttpContext.WebSockets.AcceptWebSocketAsync();
            _chatWebSocketManager.AddClient(clientId, webSocket);
            Console.WriteLine($"connected client id: {clientId}");

            await ReceiveMessageses(clientId, webSocket);
            return new EmptyResult();
        } else {
            return BadRequest();
        }
    }

    private async Task ReceiveMessageses(string senderId, WebSocket webSocket)
    {
        var buffer = new byte[1024 * 4];
        while(webSocket.State == WebSocketState.Open)
        {
            var result = await webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);
            if (result.MessageType == WebSocketMessageType.Close)
            {
                await _chatWebSocketManager.RemoveClient(senderId);
                break;
            }

            var message = Encoding.UTF8.GetString(buffer, 0, result.Count);
            var parts = message.Split(":", 2);
            if (parts.Length == 2)
            {
                var receivedId = parts[0];
                var chatMessage = parts[1];
                await _chatWebSocketManager.SendMessageAsync(receivedId, chatMessage);
                Console.WriteLine($"message sent: id {receivedId}, message {chatMessage}");
            }
        }
    }
}