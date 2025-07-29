package com.project.requestid.network

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

//class RetrofitClient {
//}

object RetrofitClient {
    private val retrofit = Retrofit.Builder().baseUrl("http://10.0.2.2:8080/request-id").addConverterFactory(GsonConverterFactory.create()).build()
    val webService: WebService = retrofit.create(WebService::class.java)
}