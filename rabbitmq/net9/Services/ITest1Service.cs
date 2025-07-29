namespace net9.Services;

public interface ITest1Service
{
    Task<string> SendMessage(string message);
}