using System.Text.Json.Serialization;

namespace net9.Models.Requests
{
    public class Test1DeleteRequest
    {
        [JsonPropertyName("id")]
        public required int Id { set; get; }
    }
}