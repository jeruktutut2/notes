using System.Text.Json.Serialization;

namespace net9.Models.Responses;

public class UpdateResponse
{
    [JsonPropertyName("id")]
    public required int Id { set; get; }

    [JsonPropertyName("test")]
    public required string Test { set; get; } = string.Empty;
}