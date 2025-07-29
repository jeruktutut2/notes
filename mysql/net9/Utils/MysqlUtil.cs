using System.Data;
using System.Linq.Expressions;
using MySql.Data.MySqlClient;

namespace net9.Utils
{
    // public class MysqlUtil : IDisposable
    // {
    //     // private readonly string _connectionString;
    //     private readonly MySqlConnection _connection;
    //     // private readonly IDbConnection? _connection;
    //     // private IDbTransaction? _transaction;
    //     private MySqlTransaction? _transaction;

    //     // public async Task<IDbConnection> Connect()
    //     // public MysqlUtil(string connectionString)
    //     public MysqlUtil(IConfiguration configuration)
    //     {
    //          try 
    //          {
    //             Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} mysql: connecting to localhost:3309");
    //             _connection = new MySqlConnection(configuration.GetConnectionString("DefaultConnection"));
    //             _connection.Open();
    //             Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} mysql: connected to localhost:3309");

    //             Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} mysql: pinging to localhost:3309");
    //             if (!_connection.Ping()) {
    //             // var ping = await Ping();
    //             // if (ping) {
    //                 Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} mysql: failed to ping to localhost:3309");
    //                 Environment.Exit(1);
    //             }
    //             Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} mysql: pinged to localhost:3309");
    //             // return _connection;
    //         }
    //         catch(Exception e)
    //         {
    //             Console.WriteLine($"error when connectiong to mysql localhost:3009: {e}");
    //             Environment.Exit(1);
    //             // return null;
    //         }

    //     }

    //     // public IDbConnection GetConnection()
    //     // {
    //     //     if ((_connection?.State ?? ConnectionState.Closed) == ConnectionState.Closed || (_connection?.State ?? ConnectionState.Broken) == ConnectionState.Broken) {
    //     //         _connection?.Open();
    //     //     }
    //     //     return _connection ?? throw new InvalidOperationException("Database connection is not initialized.");
    //     // }

    //     // public IDbConnection Connection => _connection;
    //     public MySqlConnection Connection => _connection;
    //     // public IDbTransaction Transaction => _transaction;
    //     public MySqlTransaction Transaction => _transaction;

    //     public void Begin() {
    //         _transaction = _connection.BeginTransaction();
    //         // _transaction
    //     }

    //     public void Commit() {
    //         // _transaction?.Commit();
    //         if (_transaction == null) {
    //             throw new InvalidOperationException("no active transaction to commit");
    //         } 
    //         _transaction.Commit();
    //         // _transaction = null;
    //     }

    //     public void Rollback() {
    //         if (_transaction == null) {
    //             throw new InvalidOperationException("no active transaction to rollback");
    //         }
    //         _transaction.Rollback();
    //         // _transaction = null;
    //     }

    //     // private async Task<bool> Ping()
    //     // {
    //     //     try
    //     //     {
    //     //         var result = await _connection.ExecuteScalarAsync<int>("SELECT 1;");
    //     //         return result == 1;
    //     //     }
    //     //     catch(Exception)
    //     //     {
    //     //          return false;
    //     //     }
    //     // }

    //     public void Dispose()
    //     {
    //         try
    //         {
    //             Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} mysql: closing to localhost:3309");
    //             _connection?.Close();
    //             _connection?.Dispose();
    //             Console.WriteLine($"{DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} mysql: closed to localhost:3309");
    //         }
    //         catch(Exception e)
    //         {
    //             Console.WriteLine($"error when closing mysql connection localhost:3309: {e}");
    //         }
    //         finally
    //         {
    //             GC.SuppressFinalize(this);
    //         }
    //         // GC.SuppressFinalize(this);
    //     }
    // }
}