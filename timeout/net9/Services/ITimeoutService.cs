namespace net9.Services;

public interface ITimeoutService
{
    Task<string> TimeoutWithoutTx(CancellationToken cancellationToken);
    Task<string> TimeoutWithTx(CancellationToken cancellationToken);
}