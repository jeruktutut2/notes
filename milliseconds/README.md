# MILLISECOND

## curl test
    curl -i -X GET \
        -H "Content-Type: application/json" \
        -d '{"year": 2025, "month": 5, "date": 6, "hour": 0, "minute": 0, "second": 0}' \
        http://localhost:8080/millisecond/plus8
    curl -i -X GET \
        -H "Content-Type: application/json" \
        -d '{"year": 2025, "month": 5, "date": 6, "hour": 0, "minute": 0, "second": 0}' \
        http://localhost:8080/millisecond/minus8

## android > 26 (8.0)
    // Local time 2025-05-06 00:00:00
    val localDateTime = LocalDateTime.of(2025, 5, 6, 0, 0)

    val zonePlus8 = ZoneOffset.ofHours(8)
    val zonedPlus8 = ZonedDateTime.of(localDateTime, zonePlus8)
    val plus1hPlus8 = zonedPlus8.plusHours(1)
    println("GMT+08:00 +1 jam : $plus1hPlus8")
    println("Epoch millis     : ${plus1hPlus8.toInstant().toEpochMilli()}")

    val zoneMinus8 = ZoneOffset.ofHours(-8)
    val zonedMinus8 = ZonedDateTime.of(localDateTime, zoneMinus8)
    val plus1hMinus8 = zonedMinus8.plusHours(1)
    println("GMT-08:00 +1 jam : $plus1hMinus8")
    println("Epoch millis     : ${plus1hMinus8.toInstant().toEpochMilli()}")

    val now = Instant.now()
    println("Sekarang (UTC): $now")

    val gmtPlus8 = now.plus(Duration.ofHours(8))
    val timePlus8 = ZonedDateTime.ofInstant(gmtPlus8, zonePlus8)
    println("Sekarang +8 jam (GMT+08:00): $timePlus8")
    println("Epoch millis: ${timePlus8.toInstant().toEpochMilli()}")

    val gmtMinus8 = now.minus(Duration.ofHours(8))
    val timeMinus8 = ZonedDateTime.ofInstant(gmtMinus8, zoneMinus8)
    println("Sekarang -8 jam (GMT-08:00): $timeMinus8")
    println("Epoch millis: ${timeMinus8.toInstant().toEpochMilli()}")