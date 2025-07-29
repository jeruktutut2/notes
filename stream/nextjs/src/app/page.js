'use client'

import { useEffect, useState } from "react";
import axios from "axios";

export default function Home() {
    const [data, setData] = useState([]);
    useEffect(() => {
        const fetchStream = async () => {
            try {
                // i dont know why have to put http://localhost:8080 to make stream works, or create middleware
                // const response = await fetch("http://localhost:8080/stream/stream-without-channel"); // Panggil endpoint backend
                const response = await fetch("/stream/stream-without-channel");
                if (!response.body) throw new Error("Response body is empty");
                const reader = response.body.getReader();
                const decoder = new TextDecoder();
    
                while (true) {
                    const { value, done } = await reader.read();
                    if (done) break;
    
                    const chunk = decoder.decode(value, { stream: true });
                    console.log("chunk:", chunk);
                }
            } catch (error) {
                console.error("Streaming error:", error);
            }
        };
    
        fetchStream();
    }, []);

    return (
        <>
        </>
    );
}
