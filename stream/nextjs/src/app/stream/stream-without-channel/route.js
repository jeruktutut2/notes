export async function GET(req) {
    const backendUrl = `http://localhost:8080/stream/stream-without-channel`;

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