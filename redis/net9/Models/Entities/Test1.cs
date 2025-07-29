using System.Text.Json.Serialization;

namespace net9.Models.Entities;

public class Test1
{
    [JsonPropertyName("id")]
    public required string Id { set; get ;}

    [JsonPropertyName("test")]
    public required string Test { set; get; }
}