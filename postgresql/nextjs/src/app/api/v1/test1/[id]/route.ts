import { NextResponse } from "next/server";
import { Test1Service } from "@/services/test1-service";

export async function GET(req: Request, { params }: { params: Promise<{ id: string }>}) {
    const { id } = await params
    const response = await Test1Service.getById(Number(id))
    // return NextResponse.json({}, {})
    return NextResponse.json(response.BodyResponse, {status: response.httpStatusCode})
}