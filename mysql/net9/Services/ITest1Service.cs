using net9.Models.Requests;
using net9.Models.Responses;

namespace net9.Services
{
    public interface ITest1Service
    {
        Task<Response<Test1?>> Create(Test1CreateRequest test1CreateRequest);
        Task<Response<Test1?>> GetById(int id);
        Task<Response<Test1?>> Update(Test1UpdateRequest test1UpdateRequest);
        Task<Response<MessageResponse?>> Delete(Test1DeleteRequest test1DeleteRequest);
    }
}