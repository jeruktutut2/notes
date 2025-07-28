using System.Text.Json.Serialization;

namespace net9.Models.Requests;

public class ImageRequest
{
    [JsonPropertyName("image")]
    public required string ImageBase64 { set; get; }
}