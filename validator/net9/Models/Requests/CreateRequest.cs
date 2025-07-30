using System.ComponentModel.DataAnnotations;
using System.Text.Json.Serialization;

namespace net9.Models.Requests;

public class CreateRequest
{
    [JsonPropertyName("email")]
    [Required(ErrorMessage = "email is mandatory")]
    public string Email { set; get; } = string.Empty;

    [JsonPropertyName("username")]
    [Required(ErrorMessage = "username is mandatory")]
    public string Username { set; get; } = string.Empty;

    [JsonPropertyName("phoneNumber")]
    [Required(ErrorMessage = "phoneNumber is mandatory")]
    public string PhoneNumber { set; get; } = string.Empty;

    [JsonPropertyName("password")]
    [Required(ErrorMessage = "password is mandatory")]
    public string Password { set; get; } = string.Empty;
}