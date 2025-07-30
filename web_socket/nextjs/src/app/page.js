'use client'

import Image from "next/image";
import { useEffect, useRef, useState } from "react";

export default function Home() {
  const [clientId, setClientId] = useState("");
  const [clientIdSendTo, setClientIdSendTo] = useState("");
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const ws = useRef(null);

  function connectWebSocket() {
    if (!clientId) {
      alert("Masukkan ID dulu!");
      return;
    }

    if (ws.current) {
      ws.current.close();
    }

    ws.current = new WebSocket(`ws://localhost:8080/ws?id=${clientId}`);

    ws.current.onopen = () => {
      console.log(`Terhubung sebagai ${clientId}`);
    };

    ws.current.onmessage = (event) => {
      setMessages((prevMessages) => [...prevMessages, event.data]);
    };

    ws.current.onclose = () => {
      console.log("WebSocket terputus");
    };
  };

  async function sendMessage() {
    if (!clientId) {
      alert("Hubungkan WebSocket dulu!");
      return;
    }

    if (!message) {
      alert("Masukkan pesan!");
      return;
    }

    await fetch(`http://localhost:8080/send-message?clientIdSendTo=${clientIdSendTo}&msg=${message}`);
    setMessages((prevMessages) => [...prevMessages, `Anda: ${message}`]);
    setMessage("");
  };

  useEffect(() => {
    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);
  return (
    <>
      <h1>WebSocket Client (Next.js)</h1>

      <input type="text" placeholder="Masukkan ID Anda" value={clientId} onChange={(e) => setClientId(e.target.value)} style={{ padding: "10px", margin: "5px", width: "80%" }}/>
      <button onClick={connectWebSocket} style={{ padding: "10px", cursor: "pointer" }}>Hubungkan</button>

      <br />
      <input type="text" placeholder="Masukkan ID Send To Anda" value={clientIdSendTo} onChange={(e) => setClientIdSendTo(e.target.value)} style={{ padding: "10px", margin: "5px", width: "80%" }}/>

      <br />

      <input type="text" placeholder="Ketik pesan..." value={message} onChange={(e) => setMessage(e.target.value)} style={{ padding: "10px", margin: "5px", width: "80%" }}/>
      <button onClick={sendMessage} style={{ padding: "10px", cursor: "pointer" }}>Kirim</button>

      <div style={{ marginTop: "20px", textAlign: "left" }}>
        <h3>Pesan:</h3>
        <ul>
          {messages.map((msg, index) => (
            <li key={index}>{msg}</li>
          ))}
        </ul>
      </div>

    </>
  );
}
