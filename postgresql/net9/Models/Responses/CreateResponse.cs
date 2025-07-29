using System.Text.Json.Serialization;
using Microsoft.VisualBasic;

namespace net9.Models.Responses;

public class CreateResponse
{
    [JsonPropertyName("id")]
    public required int Id { set; get; }

    [JsonPropertyName("test")]
    public required string Test { set; get; } = string.Empty;
}