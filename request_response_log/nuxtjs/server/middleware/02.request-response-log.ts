export default defineEventHandler(async (event) => {
    if (event.method !== "GET") {
        const body = await readBody(event)
        // console.log(body)
        const userAgent = getRequestHeaders(event)['user-agent'] || "Unknown"
        const remoteAddr = getRequestIP(event) || "Unknown"
        const forwardedFor = getRequestHeaders(event)['x-forwarded-for'] || "Unknown"
        console.log(`{"requestTime": "` + new Date().toISOString() + `", "app": "request-response-log", "method": "` + event.method + `","requestId":"` + event.context.uuid + `","host": "` + getRequestHeaders(event).host + `","urlPath":"` + getRequestURL(event) + `","protocol":"` + getRequestURL(event).protocol + `","body": ` + JSON.stringify(body) + `, "userAgent": "` + userAgent + `", "remoteAddr": "` + remoteAddr + `", "forwardedFor": "` + forwardedFor + `"}`)
    }

    const _write = event.node.res.write;
    const _end = event.node.res.end;
    let responseBody = '';

    event.node.res.write = function (chunk, ...args) {
        responseBody += chunk.toString();
        return _write.apply(this, [chunk, ...args]);
    };

    event.node.res.end = function (chunk, ...args) {
        if (chunk) responseBody += chunk.toString();
        // console.log('Response Body:', responseBody, "status code:", event.node.res.statusCode);
        console.log(`{"responseTime": "` + new Date().toISOString() + `", "app": "request-response-log", "requestId": "` + event.context.uuid + `", "responseStatus": ` + event.node.res.statusCode + `, "response": ` + responseBody.replace(/\n|\t/g, '') + `}`)
        return _end.apply(this, [chunk, ...args]);
    };
    // const originalHandler = event.handler;
    // event.handler = async () => {
    //     const result = await originalHandler(event);
    
    //     console.log('Response Body:', result);
    //     return result;
    // };

})