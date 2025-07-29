using Microsoft.EntityFrameworkCore;

namespace net9.Data
{
    public class AppDbContext: DbContext
    {
        public AppDbContext(DbContextOptions<AppDbContext> options): base(options)
        {
            Console.WriteLine("AppDbContext instantiated");
        }

        // protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        // {
        //     optionsBuilder.LogTo(Console.WriteLine, LogLevel.Information);
        // }

        public override void Dispose()
        {
            Console.WriteLine("AppDbContext Disposed");
            base.Dispose();
        }

        public override async ValueTask DisposeAsync()
        {
            Console.WriteLine("AppDbContext Disposed (Async)");
            await base.DisposeAsync();
        }

        public DbSet<Test1> Test1 { set; get; }
    }
}