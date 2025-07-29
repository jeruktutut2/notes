import { Test1Service } from "@/services/test1-service";
import { NextResponse } from "next/server";

export async function GET(req: Request, { params }: { params: Promise<{ id: string }>}) {
    const { id } = await params
    const httpResponse = await Test1Service.getById(Number(id))
    return NextResponse.json(httpResponse.response, { status: httpResponse.httpStatusCode })
}

export async function PUT(req: Request, { params }: { params: { id: string } }) {
    const body = await req.json()
    return NextResponse.json({"test": body}, { status: 200 })
}