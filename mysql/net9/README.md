# MYSQL

## run project
    dotnet run

## change port
    launchSettings.json -> applicationUrl

## install library
    dotnet add package Dapper
    dotnet add package MySql.Data
    dotnet add package MySql.EntityFrameworkCore --version 9.0.0
    dotnet add package Microsoft.EntityFrameworkCore.Design --version 9.0.3
    dotnet add package Microsoft.EntityFrameworkCore --version 9.0.3

## nuget
     <PackageReference Include="Microsoft.AspNetCore.OpenApi" Version="9.0.2" />
     <PackageReference Include="Microsoft.EntityFrameworkCore" Version="7.0.7" />
     <!-- <PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="9.0.2" /> -->
     <PackageReference Include="Microsoft.EntityFrameworkCore.Tools" Version="7.0.7">
      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>
      <PrivateAssets>all</PrivateAssets>
    </PackageReference>
    <PackageReference Include="MySql.Data" Version="9.2.0" />
    <PackageReference Include="MySqlConnector" Version="2.4.0" />
    <PackageReference Include="Pomelo.EntityFrameworkCore.MySql" Version="7.0.0" />

## error message
i used ```wrk -t1 -c1 -d60s http://localhost:8080/api/v1/test1/25``` and ```wrk -t2 -c2 -d60s http://localhost:8080/api/v1/test1/25``` to benchmark it. It sucess if i do ```wrk -t1 -c1 -d60s http://localhost:8080/api/v1/test1/25```, but it return error when i do ```wrk -t2 -c2 -d60s http://localhost:8080/api/v1/test1/25```
when i used db context (EF Core), it is confusing me, every request, it will instatiated and disponse, it is same with addScope
when i used addScope in program.cs, each request, mysql connection is open, i don't want it
when i used singleton in program.cs addSingleton and dapper
    MySql.Data.MySqlClient.MySqlException (0x80004005): There is already an open DataReader associated with this Connection which must be closed first.
        at MySql.Data.MySqlClient.Interceptors.ExceptionInterceptor.Throw(Exception exception)
        at MySql.Data.MySqlClient.MySqlCommand.Throw(Exception ex)
        at MySql.Data.MySqlClient.MySqlCommand.CheckState()
        at MySql.Data.MySqlClient.MySqlCommand.ExecuteReaderAsync(CommandBehavior behavior, Boolean execAsync, CancellationToken cancellationToken)
        at MySql.Data.MySqlClient.MySqlCommand.ExecuteDbDataReaderAsync(CommandBehavior behavior, CancellationToken cancellationToken)
        at Dapper.SqlMapper.QueryRowAsync[T](IDbConnection cnn, Row row, Type effectiveType, CommandDefinition command) in /_/Dapper/SqlMapper.Async.cs:line 489
        at net9.Repositories.Test1Repository.GetById(IDbConnection db, Int32 id) in /Users/macbook/Documents/note/mysql/net9/Repositories/Test1Repository.cs:line 15
        at net9.Services.Test1Service.GetById(Int32 id) in /Users/macbook/Documents/note/mysql/net9/Services/Test1Service.cs:line 37

when i used singleton in program.cs add singleton and no dapper and no ef core, pure mysql driver
    System.InvalidOperationException: Connection must be valid and open.
        at MySql.Data.MySqlClient.Interceptors.ExceptionInterceptor.Throw(Exception exception)
        at MySql.Data.MySqlClient.MySqlCommand.Throw(Exception ex)
        at MySql.Data.MySqlClient.MySqlCommand.CheckState()
        at MySql.Data.MySqlClient.MySqlCommand.ExecuteReaderAsync(CommandBehavior behavior, Boolean execAsync, CancellationToken cancellationToken)
        at MySql.Data.MySqlClient.MySqlCommand.ExecuteDbDataReaderAsync(CommandBehavior behavior, CancellationToken cancellationToken)
        at net9.Repositories.Test1Repository.GetById(MySqlConnection connection, Int32 id) in /Users/macbook/Documents/note/mysql/net9/Repositories/Test1Repository.cs:line 32
        at net9.Services.Test1Service.GetById(Int32 id) in /Users/macbook/Documents/note/mysql/net9/Services/Test1Service.cs:line 37

## tutorial
solution for ef core, make it singleton, see on video below (at minute 15):
    https://youtu.be/2t88FOeQ898?si=x7K0JEK8B6AVTyu4