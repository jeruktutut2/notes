using System.Data;
using Microsoft.EntityFrameworkCore;
using MySql.Data.MySqlClient;
using net9.Data;
using net9.Repositories;
using net9.Services;
using net9.Utils;

var builder = WebApplication.CreateBuilder(args);
// string connectionString = "server=localhost;database=test1;user=root;password=12345;port=3309;Pooling=true;Min Pool Size=5;Max Pool Size=100;Connection Timeout=30;";
// var mysqlUtil = new MysqlUtil(connectionString);
// builder.Services.AddSingleton(mysqlUtil);
// builder.Services.AddScoped<IDbConnection>(sp => {
//     string connectionString = "server=localhost;database=test1;user=root;password=12345;port=3309;Pooling=true;Min Pool Size=5;Max Pool Size=100;Connection Timeout=30;Connection Lifetime=60;";
//     return new MySqlConnection(connectionString);
// });
// builder.Services.AddScoped<MysqlUtil>();
// builder.Services.AddSingleton<MysqlUtil>();
// var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
builder.Services.AddDbContext<AppDbContext>(options => 
{
    // options.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString));
    options.UseMySQL(builder.Configuration["MySqlConnectionString"]);
}, ServiceLifetime.Singleton);
builder.Services.AddScoped<ITest1Repository, Test1Repository>();
builder.Services.AddScoped<ITest1Service, Test1Service>();
builder.Services.AddControllers();

// Add services to the container.
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

var app = builder.Build();
using (var scope = app.Services.CreateScope())
{
    var appDbContext = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    appDbContext.Database.EnsureCreated();
}
app.Lifetime.ApplicationStopping.Register(() => {
    // mysqlUtil.Dispose();
});

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
