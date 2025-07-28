namespace net9.Services;

public interface IKafkaService
{
    Task<string> SendMessage(string message);
}