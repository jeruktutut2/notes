using System.Text.Json.Serialization;

namespace net9.Models.Responses;

public class SignResponse
{
    [JsonPropertyName("message")]
    public required string Message { set; get; }
    [JsonPropertyName("signature")]
    public required string Signature { set; get; }
}