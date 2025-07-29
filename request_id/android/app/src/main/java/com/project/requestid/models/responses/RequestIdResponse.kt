package com.project.requestid.models.responses;

data class RequestIdResponse(
        val data: RequestIdData?,
        val errors: Any?
)

data class RequestIdData(
        val requestId: String
)