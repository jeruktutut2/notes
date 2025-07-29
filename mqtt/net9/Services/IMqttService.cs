namespace net9.Services;

public interface IMqttService
{
    Task<string> SendMessage(string message);
}