export interface MessageResponse {
    message: string;
}

export interface BodyResponse<T> {
    data: T | null;
    errors: Record<string, string> | null;
}

export interface Response<T> {
    httpStatusCode: number;
    response: BodyResponse<T>;
}

export function setResponse<T>(httpStatusCode: number, data: T, errors: Record<string, string>): Response<T> {
    return {
        httpStatusCode: httpStatusCode,
        response: {
            data: data,
            errors: errors
        }
    }
}

export function setOkResponse<T>(data: T): Response<T> {
    return {
        httpStatusCode: 200,
        response: {
            data: data,
            errors: null
        }
    }
}

export function setCreatedResponse<T>(data: T): Response<T> {
    return {
        httpStatusCode: 201,
        response: {
            data: data,
            errors: null
        }
    }
}

export function setNoContentResponse(message: string): Response<MessageResponse>{
    return {
        httpStatusCode: 204,
        response: {
            data: {
                message: message
            },
            errors: null
        }
    }
}

export function setBadRequestResponse(message: string): Response<null> {
    return {
        httpStatusCode: 400,
        response: {
            data: null,
            errors: {
                message: message
            }
        }
    }
}

export function setInternalServerErrorResponse(): Response<null> {
    return {
        httpStatusCode: 500,
        response: {
            data: null,
            errors: {
                message: "internal server error"
            }
        }
    }
}