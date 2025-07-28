using Microsoft.EntityFrameworkCore;
using net9.Models.Entities;

namespace net9.Context;

public class CockroachDbContext: DbContext
{
    public CockroachDbContext(DbContextOptions<CockroachDbContext> options): base(options)
    {
        Console.WriteLine("cockroachdb context is instantiated");
    }

    public override void Dispose()
    {
        Console.WriteLine("cockroachdb context disposed");
        base.Dispose();
    }

    public override async ValueTask DisposeAsync()
    {
        Console.WriteLine("cockroachdb context dispose (async)");
        await base.DisposeAsync();
    }

    public DbSet<Test1> Test1 { set; get; }
}