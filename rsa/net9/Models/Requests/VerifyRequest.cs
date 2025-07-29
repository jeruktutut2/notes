using System.Text.Json.Serialization;

namespace net9.Models.Requests;

public class VerifyRequest
{
    [JsonPropertyName("message")]
    public required string Message { set; get; }

    [JsonPropertyName("signature")]
    public required string Signature { set; get; }
}