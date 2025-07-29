using net9.Models.Requests;
using net9.Models.Responses;

namespace net9.Services;

public interface IMillisecondService
{
    Task<MillisecondResponse> GetByGMTPlus8(MillisecondRequest milliseconRequest);
    Task<MillisecondResponse> GetByGMTMinus8(MillisecondRequest milliseconRequest);
}