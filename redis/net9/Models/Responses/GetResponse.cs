using System.Text.Json.Serialization;

namespace net9.Models.Responses;

public class GetResponse
{

    [JsonPropertyName("id")]
    public required string Id { set; get; }

    [JsonPropertyName("test")]
    public required string Test { set; get;}
}