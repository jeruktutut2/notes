package com.project.requestid.network

import com.project.requestid.models.responses.RequestIdResponse
import retrofit2.http.GET

//class ApiService {
//}

interface WebService {
//    @GET("api/v1/request_id")
    @GET("request_id")
    suspend fun getRequestId(): RequestIdResponse
}