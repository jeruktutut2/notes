using Microsoft.EntityFrameworkCore;
using net9.Models.Entities;

namespace net9.Context;

public class PostgresContext: DbContext
{

    public PostgresContext(DbContextOptions<PostgresContext> options): base(options)
    {
        Console.WriteLine("postgres context is instantiated");
    }

    public override void Dispose()
    {
        Console.WriteLine("postgres context disposed");
        base.Dispose();
    }

    public override async ValueTask DisposeAsync()
    {
        Console.WriteLine("postgres disposed (async)");
        await base.DisposeAsync();
    }

    public DbSet<Test1> Test1 { set; get; }
}