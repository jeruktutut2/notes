package com.project.image.network;

interface ApiService {
    @GET("api/v1/request_id")
    suspend fun getRequestId(): RequestIdResponse
}

