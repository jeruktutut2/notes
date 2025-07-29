using System.Data;
using net9.Data;
using net9.Models.Requests;
using net9.Models.Responses;
using net9.Repositories;
using net9.Utils;

namespace net9.Services {
    // public class Test1Service(MysqlUtil mysqlUtil, ITest1Repository test1Repository) : ITest1Service
    public class Test1Service(AppDbContext appDbContext) : ITest1Service
    {
        // private readonly IDbConnection? _db = db.GetConnection();
        // private readonly MysqlUtil _mysqlUtil = mysqlUtil;
        private readonly AppDbContext _appDbContext = appDbContext;
        // private readonly ITest1Repository _test1Repository = test1Repository;

        public async Task<Response<Test1?>> Create(Test1CreateRequest test1CreateRequest)
        {
            // using var transaction = _db.BeginTransaction();
            // _mysqlUtil.Begin();
            await using var transaction = await _appDbContext.Database.BeginTransactionAsync();
            try
            {
                var test1 = new Test1 { Test = test1CreateRequest.Test};
                await _appDbContext.AddAsync(test1);
                int rowsAffected = await _appDbContext.SaveChangesAsync();
                // Console.WriteLine($"rowsAffected: {rowsAffected}");
                if (rowsAffected != 1) {
                    return ResponseHelper.SetInternalServerErrorResponse<Test1?>();
                }
                // var lastInserteId = await _test1Repository.Create(_mysqlUtil.Connection, test1, _mysqlUtil.Transaction);
                // test1.Id = (int)lastInserteId;
                // transaction.Commit();
                // _mysqlUtil.Commit();
                await transaction.CommitAsync();
                return ResponseHelper.SetCreatedResponse<Test1?>(test1);
            } catch(Exception e) {
                // transaction.Rollback();
                // _mysqlUtil.Rollback();
                Console.WriteLine(e);
                await transaction.RollbackAsync();
                return ResponseHelper.SetInternalServerErrorResponse<Test1?>();
            }
        }

        public async Task<Response<Test1?>> GetById(int id)
        {
            try
            {
                // var test1 = await _test1Repository.GetById(_mysqlUtil.Connection, id);
                var test1 = await _appDbContext.Test1.FindAsync(id);
                if (test1 == null) {
                    return ResponseHelper.SetNotFoundResponse<Test1?>($"cannot find test1 with id: {id}");
                }
                return ResponseHelper.SetOkResponse<Test1>(test1);
            }
            catch(Exception e)
            {
                Console.WriteLine(e);
                return ResponseHelper.SetInternalServerErrorResponse<Test1?>();
            }
            // return 
        }

        public async Task<Response<Test1?>> Update(Test1UpdateRequest test1UpdateRequest)
        {
            // using var transaction = _db.BeginTransaction();
            await using var transaction = await _appDbContext.Database.BeginTransactionAsync();
            try
            {
                var test1 = await _appDbContext.Test1.FindAsync(test1UpdateRequest.Id);
                if (test1 == null) {
                    return ResponseHelper.SetNotFoundResponse<Test1?>($"cannot find test1 with id: {test1UpdateRequest.Id}");
                }
                // var test1 = new Test1 { Id = test1UpdateRequest.Id, Test = test1UpdateRequest.Test};
                // var rowsAffected = await _test1Repository.Update(_mysqlUtil.Connection, test1);
                test1.Test = test1UpdateRequest.Test;
                var rowsAffected = await _appDbContext.SaveChangesAsync();
                if (rowsAffected != 1)
                {
                    return ResponseHelper.SetInternalServerErrorResponse<Test1?>();
                }
                // transaction.Commit();
                await transaction.CommitAsync();
                return ResponseHelper.SetOkResponse<Test1>(test1);
            }
            catch(Exception)
            {
                // transaction.Rollback();
                await transaction.RollbackAsync();
                return ResponseHelper.SetInternalServerErrorResponse<Test1?>();
            }
        }

        public async Task<Response<MessageResponse?>> Delete(Test1DeleteRequest test1DeleteRequest)
        {
            // using var transaction = _db.BeginTransaction();
            await using var transaction = await _appDbContext.Database.BeginTransactionAsync();
            try{
                var test1 = await _appDbContext.Test1.FindAsync(test1DeleteRequest.Id);
                if (test1 == null) {
                    return ResponseHelper.SetNotFoundResponse<MessageResponse?>($"cannot find test1 with id: {test1DeleteRequest.Id}");
                }
                // var rowsAffected = await _test1Repository.Delete(_mysqlUtil.Connection, test1DeleteRequest.Id);
                _appDbContext.Remove(test1);
                var rowsAffected = await _appDbContext.SaveChangesAsync();
                if (rowsAffected != 1) {
                    return ResponseHelper.SetInternalServerErrorResponse<MessageResponse?>();
                }
                await transaction.CommitAsync();
                var messageResponse = new MessageResponse { Message = "successfully delete test" };
                // transaction.Commit();
                return ResponseHelper.SetNoContentResponse<MessageResponse?>(messageResponse);
            }
            catch(Exception e)
            {
                // transaction.Rollback();
                Console.WriteLine(e);
                await transaction.RollbackAsync();
                return ResponseHelper.SetInternalServerErrorResponse<MessageResponse?>();
            }
        }
    }
}