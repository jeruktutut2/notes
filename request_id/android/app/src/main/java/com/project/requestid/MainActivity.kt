package com.project.requestid

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.text.BasicTextField
import androidx.compose.material3.Button
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.TextStyle
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import com.project.requestid.ui.theme.RequestIdTheme
import com.project.requestid.viewmodel.MainViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        val viewModel = MainViewModel()
        setContent {
//            RequestIdTheme {
//                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
//                    Greeting(
//                        name = "Android",
//                        modifier = Modifier.padding(innerPadding)
//                    )
//                }
//            }
            val requestId by viewModel.requestId.collectAsState()

            Box(
                modifier = Modifier.fillMaxSize().background(Color.White),
                contentAlignment = Alignment.Center
            ) {
                Column(
                    horizontalAlignment = Alignment.CenterHorizontally,
                    verticalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    BasicTextField(
                        value = requestId,
                        onValueChange = {},
                        modifier = Modifier.background(Color.Black).padding(8.dp),
                        textStyle = TextStyle(color = Color.White)
                    )
                    Button(
                        onClick = { viewModel.fetchRequestId() },
                        modifier = Modifier.background(Color.Blue).padding(8.dp)
                    ) {
                        Text("Fetch request id", color = Color.White)
                    }
                }
            }
        }
    }
}

//@Composable
//fun Greeting(name: String, modifier: Modifier = Modifier) {
//    Text(
//        text = "Hello $name!",
//        modifier = modifier
//    )
//}

//@Preview(showBackground = true)
//@Composable
//fun GreetingPreview() {
//    RequestIdTheme {
//        Greeting("Android")
//    }
//}