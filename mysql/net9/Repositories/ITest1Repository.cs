using System.Data;
using MySql.Data.MySqlClient;

namespace net9.Repositories {
    public interface ITest1Repository
    {
        // Task<long> Create(IDbConnection db, Test1 test1, IDbTransaction transaction);
        // Task<Test1?> GetById(IDbConnection db, int id);
        // Task<int> Update(IDbConnection db, Test1 test1);
        // Task<int> Delete(IDbConnection db, int id);

        // Task<long> Create(MySqlConnection connection, Test1 test1, IDbTransaction transaction);
        Task<Test1?> GetById(MySqlConnection connection, int id);
        // Task<int> Update(MySqlConnection connection, Test1 test1);
        // Task<int> Delete(MySqlConnection connection, int id);
    }
}