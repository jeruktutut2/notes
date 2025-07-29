using System.Data;
using MySql.Data.MySqlClient;

namespace net9.Repositories {

    public class Test1Repository: ITest1Repository
    {
        // public async Task<long> Create(IDbConnection db, Test1 test1, IDbTransaction transaction)
        // {
        //     return await db.ExecuteScalarAsync<long>("INSERT INTO test1(test) VALUES(@Test); SELECT LAST_INSERT_ID();", new {Test = test1.Test}, transaction: transaction);
        // }

        // public async Task<Test1?> GetById(IDbConnection db, int id) 
        // {
        //     return await db.QueryFirstOrDefaultAsync<Test1>("SELECT id, test FROM test1 WHERE id = @Id", new {Id = id});
        // }

        // public async Task<int> Update(IDbConnection db, Test1 test1)
        // {
        //     return await db.ExecuteAsync("UPDATE test1 SET test = @Test WHERE id = @Id", new {Id = test1.Id, Test = test1.Test});
        // }

        // public async Task<int> Delete(IDbConnection db, int id)
        // {
        //     return await db.ExecuteAsync("DELETE FROM test1 WHERE id = @Id", new { Id = id });
        // }

        public async Task<Test1?> GetById(MySqlConnection connection, int id)
        {
            using var command = new MySqlCommand("SELECT id, test FROM test1 WHERE id = @Id", connection);
            command.Parameters.AddWithValue("@Id", id);
            using var reader = await command.ExecuteReaderAsync();
            if (await reader.ReadAsync())
            {
                return new Test1
                {
                    Id = reader.GetInt32(0),
                    Test = reader.GetString(1)
                };
            }
            return null;
        }
    }

}