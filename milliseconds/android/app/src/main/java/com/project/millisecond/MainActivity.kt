package com.project.millisecond

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.project.millisecond.ui.theme.MillisecondTheme
import java.text.SimpleDateFormat
import java.util.Calendar
import java.util.Locale
import java.util.TimeZone
import java.util.logging.SimpleFormatter

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            MillisecondTheme {
//                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
//                    Greeting(
//                        name = "Android",
//                        modifier = Modifier.padding(innerPadding)
//                    )
//                }
                MyTextColumn()
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
//    Text(
//        text = "Hello mantap",
//        modifier = modifier
//    )
//}

@Composable
fun MyTextColumn() {
    val formaterPlus8 = SimpleDateFormat("yyyy-MM-dd HH:mm:ss z", Locale.getDefault())
    val calendarPlus8 = Calendar.getInstance(TimeZone.getTimeZone("GMT+08:00"))
    calendarPlus8.set(2025, Calendar.MAY, 6, 0, 0, 0)
    calendarPlus8.set(Calendar.MILLISECOND, 0)
    formaterPlus8.timeZone = calendarPlus8.timeZone

    val formaterMinus8 = SimpleDateFormat("yyyy-MM-dd HH:mm:ss z", Locale.getDefault())
    val calendarMinus8 = Calendar.getInstance(TimeZone.getTimeZone("GMT+08:00"))
    calendarMinus8.set(2025, Calendar.MAY, 6, 0, 0, 0)
    calendarMinus8.set(Calendar.MILLISECOND, 0)
    formaterMinus8.timeZone = calendarMinus8.timeZone

    val now = Calendar.getInstance(TimeZone.getTimeZone("UTC"))
    val formaterNow = SimpleDateFormat("yyyy-MM-dd HH:mm:ss z", Locale.getDefault())
    formaterNow.timeZone = TimeZone.getTimeZone("UTC")

    val nowPlus8 = now.clone() as Calendar
    nowPlus8.add(Calendar.HOUR_OF_DAY, 8)
//    formaterNow.timeZone = TimeZone.getTimeZone("GMT+08:00")

    val nowMinus8 = now.clone() as Calendar
    nowMinus8.add(Calendar.HOUR_OF_DAY, -8)
//    formaterNow.timeZone = TimeZone.getTimeZone("GMT-08:00")

    Column {
        Text(text = "Datetime: " + formaterPlus8.format(calendarPlus8.time))
        Text(text = "Millisecond: " + calendarPlus8.timeInMillis.toString())
        calendarPlus8.add(Calendar.HOUR_OF_DAY, 1)
        Text(text = "add1Hour: " + formaterPlus8.format(calendarPlus8.time))
        Text(text = "Add1HourMillisecond: " + calendarPlus8.timeInMillis.toString())
        Text(text = "")

        Text(text = "Datetime: " + formaterMinus8.format(calendarMinus8.time))
        Text(text = "Millisecond: " + calendarMinus8.timeInMillis.toString())
        calendarMinus8.add(Calendar.HOUR_OF_DAY, 1)
        Text(text = "add1Hour: " + formaterMinus8.format(calendarMinus8.time))
        Text(text = "Add1HourMillisecond: " + calendarMinus8.timeInMillis.toString())
        Text(text = "")

        Text(text = "now: " + formaterNow.format(now.time))
        Text(text = "now millisecond: " + now.timeInMillis.toString())
        Text(text = "")

        formaterNow.timeZone = TimeZone.getTimeZone("GMT+08:00")
        Text(text = "Datetime: " + formaterNow.format(nowPlus8.time))
        Text(text = "Millisecond: " + nowPlus8.timeInMillis.toString())
        nowPlus8.add(Calendar.HOUR_OF_DAY, 1)
        Text(text = "add1Hour: " + formaterMinus8.format(nowPlus8.time))
        Text(text = "add1HourMillisecond: " + nowPlus8.timeInMillis.toString())
        Text(text = "")

        formaterNow.timeZone = TimeZone.getTimeZone("GMT-08:00")
        Text(text = "Datetime: " + formaterNow.format(nowMinus8.time))
        Text(text = "Millisecond: " + nowMinus8.timeInMillis.toString())
        nowMinus8.add(Calendar.HOUR_OF_DAY, 1)
        Text(text = "add1Hour: " + formaterMinus8.format(nowMinus8.time))
        Text(text = "add1HourMillisecond: " + nowMinus8.timeInMillis.toString())
    }
//    Text(text = "1. ")
//    Text(text = "1. ")
//    Text(text = "1. ")
//    Text(text = "1. ")
//    Text(text = "1. ")
//    Text(text = "1. ")
//    Text(text = "1. ")
//    Text(text = "1. ")
}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    MillisecondTheme {
//        Greeting("Android")
        MyTextColumn()
    }
}