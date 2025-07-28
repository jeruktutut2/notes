namespace net9.Models.Requests;

public class UpdateRequest
{
    public required Guid Id { set; get; }
    public required string Test { set; get; }
}