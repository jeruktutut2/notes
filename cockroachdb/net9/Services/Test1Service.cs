using Microsoft.EntityFrameworkCore;
using net9.Context;
using net9.Models.Entities;
using net9.Models.Requests;
using net9.Models.Responses;

namespace net9.Services;

public class Test1Service: ITest1Service
{
    private readonly CockroachDbContext _cockroachDbContext;
    public Test1Service(CockroachDbContext cockroachDbContext)
    {
        _cockroachDbContext = cockroachDbContext;
    }

    public async Task<Response<CreateResponse>> Create(CreateRequest createRequest)
    {
        using var transaction = await _cockroachDbContext.Database.BeginTransactionAsync();
        try
        {
            var test1 = new Test1 { Id = Guid.CreateVersion7(), Test = createRequest.Test };
            await _cockroachDbContext.Test1.AddAsync(test1);
            var rowsAffected = await _cockroachDbContext.SaveChangesAsync();
            if (rowsAffected != 1) {
                return ResponseHelper.SetInternalServerErrorResponse<CreateResponse>();
            }
            await transaction.CommitAsync();
            return ResponseHelper.SetCreatedResponse<CreateResponse>(new CreateResponse{ Id = test1.Id.ToString(), Test = test1.Test });
        }
        catch(Exception e)
        {
            await transaction.RollbackAsync();
            Console.WriteLine($"error: {e}");
            return ResponseHelper.SetInternalServerErrorResponse<CreateResponse>();
        }
    }

    public async Task<Response<GetByIdResponse>> GetById(Guid id)
    {
        try
        {
            var test1 = await _cockroachDbContext.Test1.FindAsync(id);
            if (test1 is null) {
                return ResponseHelper.SetNotFoundResponse<GetByIdResponse>($"cannot find test1 with id: {id}");
            }
            return ResponseHelper.SetOkResponse<GetByIdResponse>(new GetByIdResponse{ Id = test1.Id.ToString(), Test = test1.Test });
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
            return ResponseHelper.SetInternalServerErrorResponse<GetByIdResponse>();
        }
    }

    public async Task<Response<List<GetAllResponse>>> GetAll()
    {
        try
        {
            var test1s = await _cockroachDbContext.Test1.ToListAsync();
            if (test1s.Count < 1) {
                return ResponseHelper.SetNotFoundResponse<List<GetAllResponse>>($"cannot find test1");
            }
            List<GetAllResponse> getAllResponses = new List<GetAllResponse>();
            foreach (var test1 in test1s) {
                getAllResponses.Add(new GetAllResponse{ Id = test1.Id.ToString(), Test = test1.Test });
            }
            return ResponseHelper.SetOkResponse<List<GetAllResponse>>(getAllResponses);
        }
        catch(Exception e)
        {
            Console.WriteLine($"error: {e}");
            return ResponseHelper.SetInternalServerErrorResponse<List<GetAllResponse>>();
        }
    }

    public async Task<Response<UpdateResponse>> Update(UpdateRequest updateRequest)
    {
        using var transaction = await _cockroachDbContext.Database.BeginTransactionAsync();
        try
        {
            var test1 = await _cockroachDbContext.Test1.FindAsync(updateRequest.Id);
            if (test1 is null)
            {
                return ResponseHelper.SetNotFoundResponse<UpdateResponse>($"cannot find test1 with id: {updateRequest.Id}");
            }
            test1.Test = updateRequest.Test;
            var rowsAffected = await _cockroachDbContext.SaveChangesAsync();
            if (rowsAffected != 1)
            {
                return ResponseHelper.SetInternalServerErrorResponse<UpdateResponse>();
            }
            await transaction.CommitAsync();
            return ResponseHelper.SetOkResponse<UpdateResponse>(new UpdateResponse { Id = test1.Id.ToString(), Test = test1.Test });
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
        using var transaction = await _cockroachDbContext.Database.BeginTransactionAsync();
        try
        {
            var test1 = await _cockroachDbContext.Test1.FindAsync(deleteRequest.Id);
            if (test1 is null)
            {
                return ResponseHelper.SetNotFoundResponse<MessageResponse>($"cannot find test1 with id: {deleteRequest.Id}");
            }
            _cockroachDbContext.Remove(test1);
            var rowsAffected = await _cockroachDbContext.SaveChangesAsync();
            if (rowsAffected != 1)
            {
                return ResponseHelper.SetInternalServerErrorResponse<MessageResponse>();
            }
            await transaction.CommitAsync();
            return ResponseHelper.SetNoContentResponse<MessageResponse>();
        }
        catch(Exception e)
        {
            await transaction.RollbackAsync();
            Console.WriteLine($"error: {e}");
            return ResponseHelper.SetInternalServerErrorResponse<MessageResponse>();
        }
    }
}