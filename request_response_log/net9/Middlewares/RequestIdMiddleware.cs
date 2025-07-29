// using Microsoft.AspNetCore.Http;
// using System.Threading.Tasks;

namespace net9.Middlewares {

    public class RequestIdMiddleware(RequestDelegate next)
    {
        private readonly RequestDelegate _next = next;

        public async Task InvokeAsync(HttpContext context) {
            context.Items["requestId"] = Guid.NewGuid().ToString();
            await _next(context);
        }
    }
}