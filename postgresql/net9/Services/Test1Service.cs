using Microsoft.EntityFrameworkCore;
using net9.Context;
using net9.Models.Entities;
using net9.Models.Requests;
using net9.Models.Responses;

namespace net9.Services;

public class Test1Service: ITest1Service {
    private readonly PostgresContext _postgresContext;

    public Test1Service(PostgresContext postgresContext)
    {
        _postgresContext = postgresContext;
    }

    public async Task<Response<CreateResponse>> Create(CreateRequest createRequest)
    {
        using var transaction = await _postgresContext.Database.BeginTransactionAsync();
        try
        {
            var test1 = new Test1 {Test = createRequest.Test};
            await _postgresContext.Test1.AddAsync(test1);
            int rowsAffected = await _postgresContext.SaveChangesAsync();
            if (rowsAffected != 1) {
                return ResponseHelper.SetInternalServerErrorResponse<CreateResponse>();
            }
            await transaction.CommitAsync();
            return ResponseHelper.SetCreatedResponse<CreateResponse>(new CreateResponse{Id = test1.Id, Test = test1.Test});
        }
        catch(Exception e)
        {
            await transaction.RollbackAsync();
            Console.WriteLine($"error: {e}");
            return ResponseHelper.SetInternalServerErrorResponse<CreateResponse>();
        }
    }

    public async Task<Response<GetByIdResponse>> GetById(int id)
    {
        try
        {
            var test1 = await _postgresContext.Test1.AsNoTracking().FirstOrDefaultAsync(t => t.Id == id);
            if (test1 == null) {
                return ResponseHelper.SetNotFoundResponse<GetByIdResponse>($"cannot find test1 with id: {id}");
            }
            return ResponseHelper.SetOkResponse<GetByIdResponse>(new GetByIdResponse{Id = test1.Id, Test = test1.Test});
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
            return ResponseHelper.SetInternalServerErrorResponse<GetByIdResponse>();
        }
    }

    public async Task<Response<UpdateResponse>> Update(UpdateRequest updateRequest)
    {
        using var transaction = await _postgresContext.Database.BeginTransactionAsync();
        try
        {
            var test1 = await _postgresContext.Test1.FindAsync(updateRequest.Id);
            if (test1 == null) {
                return ResponseHelper.SetNotFoundResponse<UpdateResponse>($"cannot find test1 with id: {updateRequest.Id}");
            }
            test1.Test = updateRequest.Test;
            int rowsAffected = await _postgresContext.SaveChangesAsync();
            if (rowsAffected != 1) {
                return ResponseHelper.SetInternalServerErrorResponse<UpdateResponse>();
            }
            await transaction.CommitAsync();
            return ResponseHelper.SetOkResponse<UpdateResponse>(new UpdateResponse{Id = test1.Id, Test = test1.Test});
        }
        catch(Exception e)
        {
            await transaction.RollbackAsync();
            Console.WriteLine($"error: {e}");
            return ResponseHelper.SetInternalServerErrorResponse<UpdateResponse>();
        }
    }

    public async Task<Response<MessageResponse>> Delete(DeleteRequest deleteRequest)
    {
        using var transaction = await _postgresContext.Database.BeginTransactionAsync();
        try
        {
            var test1 = await _postgresContext.Test1.FindAsync(deleteRequest.Id);
            if (test1 == null) {
                return ResponseHelper.SetNotFoundResponse<MessageResponse>($"cannot find test1 with id: {deleteRequest.Id}");
            }
            _postgresContext.Remove(test1);
            var rowsAffected = await _postgresContext.SaveChangesAsync();
            if (rowsAffected != 1) {
                return ResponseHelper.SetInternalServerErrorResponse<MessageResponse>();
            }
            await transaction.CommitAsync();
            return ResponseHelper.SetNoContentResponse<MessageResponse>(null);

        }
        catch(Exception e)
        {
            await transaction.RollbackAsync();
            Console.WriteLine($"error: {e}");
            return ResponseHelper.SetInternalServerErrorResponse<MessageResponse>();
        }
    }
}