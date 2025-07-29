using System.Text.Json.Serialization;

namespace net9.Models.Requests;

public class MillisecondRequest
{
    [JsonPropertyName("year")]
    public int Year { set; get; }
    [JsonPropertyName("month")]
    public int Month { set; get; }
    [JsonPropertyName("date")]
    public int Date { set; get; }
    [JsonPropertyName("hour")]
    public int Hour { set; get; }
    [JsonPropertyName("minute")]
    public int Minute { set; get; }
    [JsonPropertyName("second")]
    public int Second { set; get; }
}