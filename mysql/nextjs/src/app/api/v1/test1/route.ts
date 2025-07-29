import { Test1CreateRequest, Test1DeleteRequest, Test1UpdateRequest } from "@/models/requests/test1-request";
import { Test1Service } from "@/services/test1-service";
import { NextResponse } from "next/server";

export async function GET() {
    const httpResponse = await Test1Service.getById(3)
    return NextResponse.json(httpResponse.response, { status: httpResponse.httpStatusCode })
}

export async function POST(req: Request) {
    const body: Test1CreateRequest = await req.json()
    const httpResponse = await Test1Service.create(body)
    return NextResponse.json(httpResponse.response, { status: httpResponse.httpStatusCode})
}

export async function PUT(req: Request) {
    const body: Test1UpdateRequest = await req.json()
    const httpResponse = await Test1Service.update(body)
    return NextResponse.json(httpResponse.response, { status: httpResponse.httpStatusCode })
}

export async function DELETE(req: Request) {
    const body: Test1DeleteRequest = await req.json()
    await Test1Service.delete(body)
    return new Response(null, { status: 204 })
}