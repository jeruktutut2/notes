namespace net9.Helpers;

public interface IKeyHelper
{
    string Sign(string message);
    bool Verify(string message, string base64Signature);
}