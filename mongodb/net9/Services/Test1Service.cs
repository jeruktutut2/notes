using MongoDB.Bson;
using MongoDB.Driver;
using net9.Context;
using net9.Models.Entities;
using net9.Models.Requests;
using net9.Models.Responses;

namespace net9.Services;

public class Test1Service: ITest1Service
{
    private readonly IMongoCollection<Test1> _test1;

    public Test1Service(MongoDbContext mongoDbContext)
    {
        _test1 = mongoDbContext.Test1;
    }

    public async Task<Response<CreateResponse>> Create(CreateRequest createRequest)
    {
        try
        {
            var test = new Test1 {Test = createRequest.Test};
            await _test1.InsertOneAsync(test);
            return ResponseHelper.SetCreatedResponse(new CreateResponse { Id = test.Id.ToString(), Test = test.Test });
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
            return ResponseHelper.SetInternalServerErrorResponse<CreateResponse>();
        }
    }

    public async Task<Response<GetByIdResponse>> GetById(string id)
    {
        try
        {
            if (!ObjectId.TryParse(id, out var objectId)) {
                return ResponseHelper.SetBadRequestResponse<GetByIdResponse>("id is not a objectId");
            }
            var test1 = await _test1.Find(m => m.Id == objectId).FirstOrDefaultAsync();
            if (test1 == null) {
                return ResponseHelper.SetNotFoundResponse<GetByIdResponse>($"cannot find test1 with id: {id}");
            }
            return ResponseHelper.SetOkResponse(new GetByIdResponse { Id = test1.Id.ToString(), Test = test1.Test });
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
            return ResponseHelper.SetInternalServerErrorResponse<GetByIdResponse>();
        }
    }

    public async Task<Response<UpdateResponse>> Update(UpdateRequest updateRequest)
    {
        try
        {
            if (!ObjectId.TryParse(updateRequest.Id, out var objectId)) {
                return ResponseHelper.SetBadRequestResponse<UpdateResponse>("id is not objectid");
            }
            var test1 = await _test1.Find(m => m.Id == objectId).FirstOrDefaultAsync();
            if (test1 == null) {
                return ResponseHelper.SetNotFoundResponse<UpdateResponse>($"cannot find test1 with id: {updateRequest.Id}");
            }
            var updatedTest1 = Builders<Test1>.Update
                .Set(m => m.Test, updateRequest.Test);
            var result = await _test1.UpdateOneAsync(m => m.Id == objectId, updatedTest1);
            if (result.ModifiedCount == 0) {
                return ResponseHelper.SetNotFoundResponse<UpdateResponse>($"there is no updated data");
            }
            return ResponseHelper.SetOkResponse(new UpdateResponse{Id = updateRequest.Id, Test = updateRequest.Test});
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
            return ResponseHelper.SetInternalServerErrorResponse<UpdateResponse>();
        }
    }

    public async Task<Response<MessageResponse?>> Delete(DeleteRequest deleteRequest)
    {
        try
        {
            if (!ObjectId.TryParse(deleteRequest.Id, out var objectId)) {
                return ResponseHelper.SetBadRequestResponse<MessageResponse?>("id is not objectid");
            }
            var test1 = await _test1.Find(m => m.Id == objectId).FirstOrDefaultAsync();
            if (test1 == null) {
                return ResponseHelper.SetNotFoundResponse<MessageResponse?>($"cannot find test1 with id: {deleteRequest.Id}");
            }
            var result = await _test1.DeleteOneAsync(m => m.Id == objectId);
            if (result.DeletedCount == 0) {
                return ResponseHelper.SetNotFoundResponse<MessageResponse?>($"there is no updated data");
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