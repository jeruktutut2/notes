import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { v4 as uuidv4 } from 'uuid';

function requestIdMiddleware(req: NextRequest) {
    const response = NextResponse.next();
    response.headers.set("X-REQUEST-ID", uuidv4())
    return response
}

function requestResponseLogMiddleware(req: NextRequest) {
    // you cannot get request body and response body int middleware, you have to do it in (each) handler or controller
}

export function middleware(req: NextRequest) {
    let response;

    response = requestIdMiddleware(req)
    if (response?.status < 200 && response?.status > 299) return response

    return response
}