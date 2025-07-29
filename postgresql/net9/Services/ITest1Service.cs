using net9.Models.Requests;
using net9.Models.Responses;

namespace net9.Services;

public interface ITest1Service {
    Task<Response<CreateResponse>> Create(CreateRequest createRequest);
    Task<Response<GetByIdResponse>> GetById(int id);
    Task<Response<UpdateResponse>> Update(UpdateRequest updateRequest);
    Task<Response<MessageResponse>> Delete(DeleteRequest deleteRequest);
}