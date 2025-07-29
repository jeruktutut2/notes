using MongoDB.Driver;
using net9.Models.Entities;

namespace net9.Context;

public class MongoDbContext
{
    private readonly IMongoDatabase _database;

    public MongoDbContext(IConfiguration configuration)
    {
        Console.WriteLine("connecting to mongodb");
        var client = new MongoClient(configuration["MongoDB:ConnectionString"]);
        _database = client.GetDatabase(configuration["MongoDB:DatabaseName"]);

        Test1 = _database.GetCollection<Test1>("test1");
        Console.WriteLine("connected to mongodb");
    }
    public IMongoCollection<Test1> Test1 { get; }
}