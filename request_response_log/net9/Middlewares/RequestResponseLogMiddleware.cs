// using Microsoft.AspNetCore.Http;
// using System.Threading.Tasks;

using System;
using System.IO;
using System.Text;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;

namespace net9.Middlewares {

    public class RequestResponseLogModdleware(RequestDelegate next) {

        private readonly RequestDelegate _next = next;

        public async Task InvokeAsync(HttpContext context) {
            string requestId = string.Empty; 
            if (context.Items.TryGetValue("requestId", out var requestIdObj) && requestIdObj is string id) {
                requestId = id;
            }

            string requestBody = await ReadRequestBody(context);
            Console.WriteLine($"requestTime: {DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")} , app: project-backend, method:  {context.Request.Method} , requestId: {requestId} , host: {context.Request.Host.Value} , urlPath: {context.Request.Path} , protocol: {context.Request.Protocol} , body: {requestBody} , userAgent: {context.Request.Headers["User-Agent"].ToString()} , remoteAddr: {context.Connection.RemoteIpAddress?.ToString()}, forwardedFor: {context.Request.Headers["X-Forwarded-For"].ToString()}");

            var originalBodyStream = context.Response.Body;
            using var responseBodyStream = new MemoryStream();
            context.Response.Body = responseBodyStream;

            try {
                await _next(context);
                responseBodyStream.Position = 0;

                string responseBody;
                using (var reader = new StreamReader(responseBodyStream, Encoding.UTF8, leaveOpen: true))
                {
                    responseBody = await reader.ReadToEndAsync();
                }

                var statusCode = context.Response.StatusCode;
                Console.WriteLine($"responseTime: {DateTime.UtcNow.ToString("yyyy-MM-dd HH:mm:ss")}, app: project-backend, requestId: {requestId}, responseStatus: {statusCode}, response: {responseBody}");
                responseBodyStream.Position = 0;
                await responseBodyStream.CopyToAsync(originalBodyStream);
            }
            finally
            {
                context.Response.Body = originalBodyStream;
            }
        }

        private async Task<string> ReadRequestBody(HttpContext context)
        {
            context.Request.EnableBuffering();

            using (StreamReader reader = new StreamReader(
                context.Request.Body, Encoding.UTF8, leaveOpen: true))
            {
                string body = await reader.ReadToEndAsync();
                context.Request.Body.Position = 0;
                return body;
            }
        }
    }

}