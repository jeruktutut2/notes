using System.Text.Json.Serialization;

namespace net9.Models.Responses;

public class MessageResponse(string message)
{
    [JsonPropertyName("message")]
    public string Message { set; get; } = message;
}

public class BodyResponse<T>(T? data, Dictionary<string, string>? errors)
{
    [JsonPropertyName("data")]
    public T? Data { set; get; } = data;

    [JsonPropertyName("errors")]
    public Dictionary<string, string>? Errors { set; get; } = errors;
}

public class Response<T>(int httpStatusCode, BodyResponse<T> bodyResponse)
{
    public int HttpStatusCode { set; get; } = httpStatusCode;
    public BodyResponse<T> BodyResponse { set; get; } = bodyResponse;
}

public static class ResponseHelper
{
    public static Response<T> SetResponse<T>(int httpStatusCode, T? data, Dictionary<string, string>? errors)
    {
        return new Response<T>(httpStatusCode, new BodyResponse<T>(data, errors));
    }

    public static Response<T> SetOkResponse<T>(T? data)
    {
        return new Response<T>(200, new BodyResponse<T>(data, null));
    }

    public static Response<T> SetCreatedResponse<T>(T data)
    {
        return new Response<T>(201, new BodyResponse<T>(data, null));
    }

    public static Response<T?> SetNoContentResponse<T>(T? data)
    {
        return new Response<T?>(204, new BodyResponse<T?>(data, null));
    }

    public static Response<T> SetBadRequestResponse<T>(string message)
    {
        return new Response<T>(400, new BodyResponse<T>(default, new Dictionary<string, string>{{"message", message}}));
    }

    public static Response<T> SetNotFoundResponse<T>(string message)
    {
        return new Response<T>(404, new BodyResponse<T>(default, new Dictionary<string, string>{{"message", message}}));
    }

    public static Response<T> SetInternalServerErrorResponse<T>()
    {
        return new Response<T>(500, new BodyResponse<T>(default, new Dictionary<string, string>{{ "message", "internal server error"}}));
    }
}