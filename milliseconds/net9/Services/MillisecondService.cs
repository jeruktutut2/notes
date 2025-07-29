using net9.Models.Requests;
using net9.Models.Responses;

namespace net9.Services;

public class MillisecondService: IMillisecondService
{
    public MillisecondService()
    {
        
    }

    public async Task<MillisecondResponse> GetByGMTPlus8(MillisecondRequest milliseconRequest)
    {
        var plus8 = new DateTimeOffset(milliseconRequest.Year, milliseconRequest.Month, milliseconRequest.Date, milliseconRequest.Hour, milliseconRequest.Minute, milliseconRequest.Second, TimeSpan.FromHours(8));
        var plus8Add1Hour = plus8.AddHours(1);
        
        return new MillisecondResponse{
            Datetime = plus8.ToString(),
            Millisecond = plus8.ToUnixTimeMilliseconds(),
            Add1Hour = plus8Add1Hour.ToString(),
            Add1HourMillisecond = plus8Add1Hour.ToUnixTimeMilliseconds()
        };
    }

    public async Task<MillisecondResponse> GetByGMTMinus8(MillisecondRequest milliseconRequest)
    {
        var minus8 = new DateTimeOffset(milliseconRequest.Year, milliseconRequest.Month, milliseconRequest.Date, milliseconRequest.Hour, milliseconRequest.Minute, milliseconRequest.Second, TimeSpan.FromHours(-8));
        var minus8Add1Hour = minus8.AddHours(1);
        return new MillisecondResponse{
            Datetime = minus8.ToString(),
            Millisecond = minus8.ToUnixTimeMilliseconds(),
            Add1Hour = minus8Add1Hour.ToString(),
            Add1HourMillisecond = minus8Add1Hour.ToUnixTimeMilliseconds()
        };
    }
}