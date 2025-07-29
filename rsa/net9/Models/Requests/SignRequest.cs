using System.Text.Json.Serialization;

namespace net9.Models.Requests;

public class SignRequest
{
    [JsonPropertyName("message")]
    public required string Message { set; get; }
}