package com.project.kafka.network;

//public class ApiService {
//}

interface ApiService {
    @GET("api/v1/request_id")
    suspend fun getRequestId(): RequestIdResponse
}
