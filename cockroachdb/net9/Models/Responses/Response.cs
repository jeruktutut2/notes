using System.Text.Json.Serialization;

namespace net9.Models.Responses;

public class MessageResponse {
    [JsonPropertyName("message")]
    public required string Message { set; get; }
}

public class BodyResponse<T>(T? data, Dictionary<string, string>? errors)
{
    [JsonPropertyName("data")]
    public T? Data { set; get; } = data;

    [JsonPropertyName("errors")]
    public Dictionary<string, string>? Errors { set; get; } = errors;
}

public class Response<T>(int httpStatusCode, T? data, Dictionary<string, string>? errors)
{
    [JsonPropertyName("httpStatusCode")]
    public int HttpStatuscode { set; get; } = httpStatusCode;

    [JsonPropertyName("bodyResponse")]
    public BodyResponse<T> BodyResponse { set; get; } = new BodyResponse<T>(data, errors);
}

public static class ResponseHelper
{
    public static Response<T> SetResponse<T>(int httpStatusCode, T? data, Dictionary<string, string> errors)
    {
        return new Response<T>(httpStatusCode, data, errors);
    }
    
    public static Response<T?> SetOkResponse<T>(T? data)
    {
        return new Response<T?>(200, data, null);
    }

    public static Response<T> SetCreatedResponse<T>(T data)
    {
        return new Response<T>(201, data, null);
    }
    
    public static Response<T> SetNoContentResponse<T>()
    {
        return new Response<T>(204, default, null);
    }
    
    public static Response<T> SetBadRequestResponse<T>(string message)
    {
        return new Response<T>(400, default , new Dictionary<string, string>{{"message", message}});
    }
    
    public static Response<T> SetNotFoundResponse<T>(string message) {
        return new Response<T>(404, default, new Dictionary<string, string>{{"message", message}});
    }
    
    public static Response<T> SetInternalServerErrorResponse<T>()
    {
        return new Response<T>(500, default, new Dictionary<string, string>{{"message", "internal server error"}});
    }
}