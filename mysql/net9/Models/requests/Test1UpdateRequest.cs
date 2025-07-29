using System.Text.Json.Serialization;

namespace net9.Models.Requests
{
    public class Test1UpdateRequest
    {
        [JsonPropertyName("id")]
        public required int Id { set; get; }
        [JsonPropertyName("test")]
        public required string Test { set; get; }

    }
}