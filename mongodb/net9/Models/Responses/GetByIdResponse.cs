using System.Text.Json.Serialization;
using MongoDB.Bson;

namespace net9.Models.Responses;

public class GetByIdResponse
{
    [JsonPropertyName("id")]
    public required string Id { set; get; }

    [JsonPropertyName("test")]
    public required string Test { set; get; }

}