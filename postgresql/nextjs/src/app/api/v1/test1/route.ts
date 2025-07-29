import { CreateRequest } from "@/models/requests/create-request";
import { NextResponse } from "next/server";
import { Test1Service } from "@/services/test1-service";
import { UpdateRequest } from "@/models/requests/update-request";
import { DeleteRequest } from "@/models/requests/delete-request";

export async function GET() {
    return NextResponse.json({}, {})
}

export async function POST(req: Request) {
    const body: CreateRequest = await req.json()
    const response = await Test1Service.create(body)
    return NextResponse.json(response.BodyResponse, {status: response.httpStatusCode})
}

export async function PUT(req: Request) {
    const body: UpdateRequest = await req.json()
    const response = await Test1Service.update(body)
    return NextResponse.json(response.BodyResponse, {status: response.httpStatusCode})
}

export async function DELETE(req: Request) {
    const body: DeleteRequest = await req.json()
    const response = await Test1Service.delete(body)
    // return NextResponse.json(null, {status: response.httpStatusCode})
    return new Response(null, {status: response.httpStatusCode})
}