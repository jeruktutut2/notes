export async function GET(req, res) {
    res.setHeader('Content-Type', 'text/event-stream');
    res.setHeader('Cache-Control', 'no-cache');
    res.setHeader('Connection', 'keep-alive');
    res.socket.setTimeout(0);
    
    const backendUrl = `http://localhost:8080/sse/handle-sse-without-channel-2?id=1`;

    const backendRes = await fetch(backendUrl, {
        method: "GET",
        headers: req.headers,
    });

    return new Response(backendRes.body, {
        headers: {
            "Content-Type": backendRes.headers.get("Content-Type") || "text/plain",
            "Transfer-Encoding": "chunked",
        },
    });
}