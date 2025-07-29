using net9.Models.Requests;
using net9.Models.Responses;

namespace net9.Services;

public interface ITest1Service {
    Task<Response<CreateResponse>> Create(CreateRequest createRequest);
    Task<Response<GetResponse>> Get(string id);
    Task<Response<MessageResponse?>> Delete(DeleteRequest deleteRequest);
}