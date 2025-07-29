using net9.Consumers;
using net9.Services;
using net9.Utils;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();
var rabbitmqUtil = new RabbitMQUtil();
await rabbitmqUtil.InitializeAsync();
builder.Services.AddSingleton(rabbitmqUtil);
builder.Services.AddSingleton(sp => sp.GetRequiredService<RabbitMQUtil>().GetChannel());

builder.Services.AddScoped<ITest1Service, Test1Servive>();
builder.Services.AddHostedService<RabbitMQConsumer>();
builder.Services.AddControllers();

var app = builder.Build();

var lifetime = app.Services.GetRequiredService<IHostApplicationLifetime>();
lifetime.ApplicationStopping.Register(async () => await rabbitmqUtil.DisposeAsync());

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
// app.Run();
await app.RunAsync();

record WeatherForecast(DateOnly Date, int TemperatureC, string? Summary)
{
    public int TemperatureF => 32 + (int)(TemperatureC / 0.5556);
}