using System.Diagnostics;

namespace net9.Services;

public class StacktraceService: IStacktraceService
{
    public string EnvirontmentStacktrace()
    {
        string stacktrace = Environment.StackTrace;
        Console.WriteLine(stacktrace);
        return "environtment stacktrace";
    }

    public string ExceptionStacktrace()
    {
        try
        {
            throw new Exception("error happen");
        }
        catch(Exception e)
        {
            Console.WriteLine(e.StackTrace);
            return "error";
        }
    }

    public string PrintStacktrace()
    {
        StackTrace stacktrace = new StackTrace(true);
        Console.WriteLine(stacktrace.ToString());
        return "ok";
    }
}