export interface MessageResponse {
    message: string;
}

export interface BodyResponse<T> {
    data: T | null;
    errors: Record<string, string> | null;
}

export interface Response<T> {
    httpStatusCode: number;
    BodyResponse: BodyResponse<T>;
}

export function setResponse<T>(httpStatusCode: number, data: T, errors: Record<string, string>): Response<T> {
    return {
        httpStatusCode: httpStatusCode,
        BodyResponse: {
            data: data,
            errors: errors
        }
    }
}

export function setOkResponse<T>(data: T): Response<T> {
    return {
        httpStatusCode: 200,
        BodyResponse: {
            data: data,
            errors: null
        }
    }
}

export function setCreatedResponse<T>(data: T): Response<T> {
    return {
        httpStatusCode: 201,
        BodyResponse: {
            data: data,
            errors: null
        }
    }
}

export function setNoContentResponse<T>(data: T): Response<T> {
    return {
        httpStatusCode: 204,
        BodyResponse: {
            data: data,
            errors: null
        }
    }
}

export function setBadRequestResponse(message: string): Response<null>{
    return {
        httpStatusCode: 400,
        BodyResponse: {
            data: null,
            errors: {
                message: message
            }
        }
    }
}

export function setNotFoundResponse(message: string): Response<null> {
    return {
        httpStatusCode: 404,
        BodyResponse: {
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
        BodyResponse: {
            data: null,
            errors: {
                message: "internal server error"
            }
        }
    }
}