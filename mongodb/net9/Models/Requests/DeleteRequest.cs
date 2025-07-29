using System.Text.Json.Serialization;

namespace net9.Models.Requests;

public class DeleteRequest
{
    [JsonPropertyName("id")]
    public required string Id { set; get; }
}