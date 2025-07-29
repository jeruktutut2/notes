'use client'

import Image from "next/image";
import { useEffect, useState } from "react";

export default function Home() {
    useEffect(() => {
        // const eventSource = new EventSource("http://localhost:8080/sse/handle-sse-without-channel");
        const eventSource = new EventSource("/sse/handle-sse-without-channel-2?id=1");
        eventSource.onmessage = (event) => {
            console.log("SSE Data:", event.data);
            console.log("event:", event);
        }
        eventSource.onerror = (error) => {
            console.log("error:", error);
        }
        return () => {
            eventSource.close();
        };
    }, [])
    return (
      <></>
    );
}
