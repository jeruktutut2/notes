using System.Text.Json.Serialization;

namespace net9.Models.Responses;

public class VerifyResponse
{
    [JsonPropertyName("message")]
    public required string Message { set; get; }
    [JsonPropertyName("signature")]
    public required string Signature { set; get; }
    [JsonPropertyName("isVerified")]
    public required bool IsVerified { set; get; }
}