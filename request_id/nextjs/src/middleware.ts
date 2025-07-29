import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { v4 as uuidv4 } from 'uuid';

// middleware only available in root app, and only use only one function middleware(req: NextRequest)
// if you want to create more functions, just create it, and call it in middleware(req: NextRequest)
// optional: use matcher if you want to run middleware for spesific route
export function middleware(req: NextRequest) {
    const response = NextResponse.next();
    response.headers.set("X-REQUEST-ID", uuidv4())
    return response
}

// export const config = {
//     matcher: ['/dashboard/:path*', '/profile/:path*'], // Middleware for spesific routes
// };