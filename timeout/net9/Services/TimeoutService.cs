using Microsoft.EntityFrameworkCore;
using net9.Contexts;
using net9.Models.Entities;

namespace net9.Services;

public class TimeoutService: ITimeoutService
{
    private readonly PostgresContext _postgresContext;
    public TimeoutService(PostgresContext postgresContext)
    {
        _postgresContext = postgresContext;
    }
    public async Task<string> TimeoutWithoutTx(CancellationToken cancellationToken)
    {
        try
        {
            Console.WriteLine("insert test1 1");
            Test1 test1 = new() { Test = $"test1 1 {DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")}"};
            await _postgresContext.Test1.AddAsync(test1, cancellationToken);
            await _postgresContext.SaveChangesAsync(cancellationToken);

            Console.WriteLine("wait test1 1");
            await _postgresContext.Database.ExecuteSqlRawAsync("SELECT pg_sleep(3);", cancellationToken: cancellationToken);

            Console.WriteLine("insert test1 2");
            test1 = new() { Test = $"test1 2 {DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")}"};
            await _postgresContext.Test1.AddAsync(test1, cancellationToken);
            await _postgresContext.SaveChangesAsync(cancellationToken);

            Console.WriteLine("wait test1 2");
            await _postgresContext.Database.ExecuteSqlRawAsync("SELECT pg_sleep(3);", cancellationToken: cancellationToken);

            Console.WriteLine("insert test1 3");
            test1 = new() { Test = $"test1 2 {DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")}"};
            await _postgresContext.Test1.AddAsync(test1, cancellationToken);
            await _postgresContext.SaveChangesAsync(cancellationToken);

            return "ok";
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
            return "error";
        }
    }

    public async Task<string> TimeoutWithTx(CancellationToken cancellationToken)
    {
        using var transaction = await _postgresContext.Database.BeginTransactionAsync(cancellationToken);
        try
        {
            Console.WriteLine("insert test1 1");
            Test1 test1 = new() { Test = $"test1 1 {DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")}"};
            await _postgresContext.Test1.AddAsync(test1, cancellationToken);
            await _postgresContext.SaveChangesAsync(cancellationToken);

            Console.WriteLine("wait test1 1");
            await _postgresContext.Database.ExecuteSqlRawAsync("SELECT pg_sleep(3);", cancellationToken: cancellationToken);

            Console.WriteLine("insert test1 2");
            test1 = new() { Test = $"test1 2 {DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")}"};
            await _postgresContext.Test1.AddAsync(test1, cancellationToken);
            await _postgresContext.SaveChangesAsync(cancellationToken);

            Console.WriteLine("wait test1 2");
            await _postgresContext.Database.ExecuteSqlRawAsync("SELECT pg_sleep(3);", cancellationToken: cancellationToken);

            Console.WriteLine("insert test1 3");
            test1 = new() { Test = $"test1 2 {DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")}"};
            await _postgresContext.Test1.AddAsync(test1, cancellationToken);
            await _postgresContext.SaveChangesAsync(cancellationToken);

            await transaction.CommitAsync(cancellationToken);
            
            return "ok";
        }
        catch(Exception e)
        {
            await transaction.RollbackAsync(cancellationToken);
            Console.WriteLine($"error: {e}");
            return "error";
        }
    }
}