using System.Text.Json.Serialization;

namespace net9.Models.Responses;

public class MillisecondResponse
{
    [JsonPropertyName("datetime")]
    public required string Datetime { set; get; }
    [JsonPropertyName("millisecond")]
    public required long Millisecond { set; get; }
    [JsonPropertyName("add1Hour")]
    public required string Add1Hour { set; get; }
    [JsonPropertyName("add1HourMillisecond")]
    public required long Add1HourMillisecond { set; get; }

}