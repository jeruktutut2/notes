export async function GET(req: Request) {
    const requestId = req.headers.get('X-REQUEST-ID')
    return Response.json({"test": requestId})
}

export async function POST(req: Request) {
    const requestId = req.headers.get('X-REQUEST-ID')
    return Response.json({"test": requestId})
}