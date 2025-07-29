package com.project.stream

import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import okhttp3.OkHttpClient
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import okhttp3.Request
import java.io.BufferedReader
import java.io.InputStreamReader

data class StreamData(val message: String, val time: String)

class StreamViewModel: ViewModel() {
    private val _dataList = MutableStateFlow<List<StreamData>>(emptyList())
    val dataList: StateFlow<List<StreamData>> get() = _dataList

    private val client = OkHttpClient()

    fun startStreaming() {
        viewModelScope.launch(Dispatchers.IO) {
            val request = Request.Builder()
                .url("http://10.0.2.2:8080/stream/stream-without-channel") // 10.0.2.2 untuk localhost dari emulator
                .build()

            client.newCall(request).execute().use { response ->
                if (!response.isSuccessful) return@use

                response.body?.let { body ->
                    val reader = BufferedReader(InputStreamReader(body.byteStream()))

                    reader.useLines { lines ->
                        lines.forEach { line ->
                            val parts = line.split(",")
                            if (parts.size == 2) {
                                val data = StreamData(
                                    message = parts[0].substringAfter(":").trim('"'),
                                    time = parts[1].substringAfter(":").trim('"', '}')
                                )
                                _dataList.value = _dataList.value + data
                            }
                        }
                    }
                }
            }
        }
    }
}