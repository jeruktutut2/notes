namespace net9.Services;

public interface IStacktraceService {
    string EnvirontmentStacktrace();
    string ExceptionStacktrace();
    string PrintStacktrace();
}