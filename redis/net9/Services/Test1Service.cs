using System.Text.Json;
using net9.Models.Entities;
using net9.Models.Requests;
using net9.Models.Responses;
using net9.Utils;
using StackExchange.Redis;

namespace net9.Services;

public class Test1Service: ITest1Service {

    private readonly IDatabase _db;

    public Test1Service(RedisUtil redisUtil) {
        _db = redisUtil.GetDatabase();
    }

    public async Task<Response<CreateResponse>> Create(CreateRequest createRequest) {
        try
        {
            Test1 test1 = new() { Id = Guid.NewGuid().ToString(), Test = createRequest.Test};
            bool isSaved = await _db.StringSetAsync(test1.Id, JsonSerializer.Serialize(test1));
            if (!isSaved) {
                Console.WriteLine($"cannot save to redis: {isSaved}");
                return ResponseHelper.SetInternalServerErrorResponse<CreateResponse>();
            }
            return ResponseHelper.SetCreatedResponse(new CreateResponse { Id = test1.Id, Test = test1.Test});
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
            return ResponseHelper.SetInternalServerErrorResponse<CreateResponse>();
        }
    }

    public async Task<Response<GetResponse>> Get(string id) {
        try
        {
            var data = await _db.StringGetAsync(id);
            if (data.IsNullOrEmpty) {
                return ResponseHelper.SetNotFoundResponse<GetResponse>($"cannot find test1 with id: {id}");
            }
            var test1 = JsonSerializer.Deserialize<Test1>(data!);
            return ResponseHelper.SetOkResponse(new GetResponse{Id = test1.Id, Test = test1.Test});
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
            return ResponseHelper.SetInternalServerErrorResponse<GetResponse>();
        }
    }

    public async Task<Response<MessageResponse?>> Delete(DeleteRequest deleteRequest) {
        try
        {
            bool isDeleted = await _db.KeyDeleteAsync(deleteRequest.Id);
            if (!isDeleted) {
                return ResponseHelper.SetInternalServerErrorResponse<MessageResponse?>();
            }
            return ResponseHelper.SetNoContentResponse<MessageResponse>(null);
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
            return ResponseHelper.SetInternalServerErrorResponse<MessageResponse?>();
        }
    }
}