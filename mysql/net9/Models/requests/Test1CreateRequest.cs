using System.Text.Json.Serialization;

namespace net9.Models.Requests {
    public class Test1CreateRequest
    {
        [JsonPropertyName("test")]
        public required string Test { set; get; }
    }
}