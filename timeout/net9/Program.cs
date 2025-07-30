using Microsoft.EntityFrameworkCore;
using net9.Contexts;
using net9.Middlewares;
using net9.Services;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();
builder.Services.AddControllers();
builder.Services.AddScoped<ITimeoutService, TimeoutService>();
builder.Services.AddDbContext<PostgresContext>(optionsBuilder =>
{
    optionsBuilder.UseNpgsql(builder.Configuration["PostgresConnectionString"]);
}, ServiceLifetime.Singleton);

var app = builder.Build();
using (var scope = app.Services.CreateScope())
{
    var postgresContext = scope.ServiceProvider.GetRequiredService<PostgresContext>();
    postgresContext.Database.EnsureCreated();
}
app.UseMiddleware<TimeoutMiddleware>();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseHttpsRedirection();

var summaries = new[]
{
    "Freezing", "Bracing", "Chilly", "Cool", "Mild", "Warm", "Balmy", "Hot", "Sweltering", "Scorching"
};

app.MapGet("/weatherforecast", () =>
{
    var forecast =  Enumerable.Range(1, 5).Select(index =>
        new WeatherForecast
        (
            DateOnly.FromDateTime(DateTime.Now.AddDays(index)),
            Random.Shared.Next(-20, 55),
            summaries[Random.Shared.Next(summaries.Length)]
        ))
        .ToArray();
    return forecast;
})
.WithName("GetWeatherForecast");

app.UseRouting();
app.MapControllers();
app.Run();

record WeatherForecast(DateOnly Date, int TemperatureC, string? Summary)
{
    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
}
