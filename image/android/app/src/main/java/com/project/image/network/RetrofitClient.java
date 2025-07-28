package com.project.image.network;

//public class RetrofitClient {
//}

object RetrofitClient {
private val retrofit = Retrofit.Builder()
        .baseUrl("https://your-api-url.com/") // Ganti dengan URL kamu
        .addConverterFactory(GsonConverterFactory.create())
        .build()

val api: ApiService = retrofit.create(ApiService::class.java)
}
