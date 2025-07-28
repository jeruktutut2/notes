using net9.Models.Entities;
using net9.Models.Requests;
using net9.Models.Responses;

namespace net9.Services;

public interface ITest1Service
{
    Task<Response<CreateResponse>> Create(CreateRequest createRequest);
    Task<Response<GetByIdResponse>> GetById(Guid id);
    Task<Response<List<GetAllResponse>>> GetAll();
    Task<Response<UpdateResponse>> Update(UpdateRequest updateRequest);
    Task<Response<MessageResponse>> Delete(DeleteRequest deleteRequest);
}