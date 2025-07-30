namespace net9.Middlewares;

public class TimeoutMiddleware
{
    private readonly RequestDelegate _next;
    
    public TimeoutMiddleware(RequestDelegate next)
    {
        _next = next;
    }

    public async Task Invoke(HttpContext context)
    {
        using var timeoutCts = new CancellationTokenSource(TimeSpan.FromSeconds(10));
        using var linkedCts = CancellationTokenSource.CreateLinkedTokenSource(timeoutCts.Token, context.RequestAborted);

        context.Items["RequestTimeoutToken"] = linkedCts.Token;

        try
        {
            await _next(context);
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
            context.Response.StatusCode = 408;
            await context.Response.WriteAsync("Request timeout");
        }
    }
}