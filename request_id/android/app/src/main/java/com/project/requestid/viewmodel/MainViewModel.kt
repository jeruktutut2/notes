package com.project.requestid.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.project.requestid.network.RetrofitClient
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class MainViewModel: ViewModel() {
    private val _requestId = MutableStateFlow("No request id")
    val requestId: StateFlow<String> = _requestId

    fun fetchRequestId() {
        viewModelScope.launch {
            try {
                val response = RetrofitClient.webService.getRequestId()
                response.data?.requestId?.let {
                    _requestId.value = it
                }
            } catch(e: Exception) {
                _requestId.value = "Error: ${e.localizedMessage}"
            }
        }
    }
}