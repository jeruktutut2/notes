using System.Text.Json.Serialization;

namespace net9.Models.Requests;

public class CreateRequest
{
    [JsonPropertyName("message")]
    public required string Message { set; get; }
}