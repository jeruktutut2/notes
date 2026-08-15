"""
=================================================================
4. STREAMING OUTPUT
=================================================================
Streaming = mengirimkan token/kata satu per satu ke client
begitu dihasilkan, BUKAN menunggu seluruh respons selesai.

Mengapa streaming penting?
- LLM besar bisa butuh 5-30 detik untuk generate response penuh
- Tanpa streaming: User menunggu loading... loading... (bad UX)
- Dengan streaming: User langsung melihat kata per kata (good UX)

Analogi:
- Non-streaming: Download file → baru bisa baca (menunggu)
- Streaming: Nonton video YouTube → langsung mulai nonton

Protokol Streaming:
- Server-Sent Events (SSE) → paling umum untuk LLM
- WebSocket → bidirectional
- gRPC streaming → high-performance
=================================================================
"""

from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer
import torch
import time
import sys


def demo_non_streaming():
    """Demo inference non-streaming (menunggu seluruh output)."""
    print("=" * 60)
    print("DEMO 1: Non-Streaming (Menunggu Seluruh Output)")
    print("=" * 60)

    nama_model = "distilgpt2"
    tokenizer = AutoTokenizer.from_pretrained(nama_model)
    model = AutoModelForCausalLM.from_pretrained(nama_model)
    model.eval()

    prompt = "The key principles of good software engineering are"
    inputs = tokenizer(prompt, return_tensors="pt")

    print(f"\n📝 Prompt: \"{prompt}\"")
    print(f"⏳ Generating... (menunggu seluruh output)")

    start = time.time()
    with torch.no_grad():
        output = model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.7,
        )
    elapsed = (time.time() - start) * 1000

    teks = tokenizer.decode(output[0], skip_special_tokens=True)
    print(f"\n💬 Output (muncul sekaligus setelah {elapsed:.0f}ms):")
    print(f"   {teks}")


def demo_streaming_textstreamer():
    """Demo streaming dengan Hugging Face TextStreamer."""
    print("\n" + "=" * 60)
    print("DEMO 2: Streaming dengan TextStreamer")
    print("=" * 60)

    nama_model = "distilgpt2"
    tokenizer = AutoTokenizer.from_pretrained(nama_model)
    model = AutoModelForCausalLM.from_pretrained(nama_model)
    model.eval()

    prompt = "Five important tips for learning artificial intelligence are"
    inputs = tokenizer(prompt, return_tensors="pt")

    print(f"\n📝 Prompt: \"{prompt}\"")
    print(f"💬 Output (streaming — muncul kata per kata):")
    print()

    # TextStreamer mencetak token begitu di-generate
    streamer = TextStreamer(tokenizer, skip_special_tokens=True)

    start = time.time()
    with torch.no_grad():
        model.generate(
            **inputs,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.7,
            streamer=streamer,  # <-- Kunci streaming!
        )
    elapsed = (time.time() - start) * 1000

    print(f"\n⏱️ Total waktu: {elapsed:.0f}ms")
    print(f"   (Tapi user sudah melihat output dari detik pertama!)")


def demo_custom_streamer():
    """Demo custom streamer untuk kontrol penuh atas streaming."""
    print("\n" + "=" * 60)
    print("DEMO 3: Custom Streamer (Kontrol Penuh)")
    print("=" * 60)

    from transformers import TextIteratorStreamer
    from threading import Thread

    nama_model = "distilgpt2"
    tokenizer = AutoTokenizer.from_pretrained(nama_model)
    model = AutoModelForCausalLM.from_pretrained(nama_model)
    model.eval()

    prompt = "The most exciting thing about AI engineering is"
    inputs = tokenizer(prompt, return_tensors="pt")

    print(f"\n📝 Prompt: \"{prompt}\"")
    print(f"💬 Output (custom streaming dengan timing info):\n")

    # TextIteratorStreamer memungkinkan iterasi token
    streamer = TextIteratorStreamer(tokenizer, skip_special_tokens=True)

    # Generate di thread terpisah (agar tidak blocking)
    generation_kwargs = dict(
        **inputs,
        max_new_tokens=80,
        do_sample=True,
        temperature=0.7,
        streamer=streamer
    )
    thread = Thread(target=model.generate, kwargs=generation_kwargs)

    start = time.time()
    thread.start()

    # Iterasi token satu per satu
    token_count = 0
    first_token_time = None
    for token_text in streamer:
        if first_token_time is None and len(token_text.strip()) > 0:
            first_token_time = (time.time() - start) * 1000
        token_count += 1
        sys.stdout.write(token_text)
        sys.stdout.flush()

    thread.join()
    total_time = (time.time() - start) * 1000

    print(f"\n\n⚡ Metrik Streaming:")
    print(f"   Time to First Token (TTFT): {first_token_time:.0f}ms" if first_token_time else "   TTFT: N/A")
    print(f"   Total waktu               : {total_time:.0f}ms")
    print(f"   Total token chunks         : {token_count}")

    print("""
    💡 METRIK PENTING STREAMING:
    
    1. TTFT (Time to First Token)
       - Waktu dari request hingga token pertama muncul
       - Target: <500ms untuk UX yang baik
       - Dipengaruhi oleh: prompt processing (prefill)
    
    2. TPS (Tokens Per Second)  
       - Kecepatan generate token setelah token pertama
       - Target: >30 TPS untuk pengalaman "mengetik" yang natural
       - Manusia membaca ~3-5 kata/detik ≈ 4-7 TPS
    
    3. Total Latency
       - TTFT + (jumlah_token / TPS)
       - Streaming membuat total latency terasa lebih pendek
    """)


def demo_sse_pattern():
    """Pola Server-Sent Events untuk streaming di production."""
    print("=" * 60)
    print("DEMO 4: Pattern SSE untuk Production API")
    print("=" * 60)

    print("""
    📋 IMPLEMENTASI STREAMING DI PRODUCTION:

    1. FastAPI + SSE (Server-Sent Events):
    
    ```python
    from fastapi import FastAPI
    from fastapi.responses import StreamingResponse
    from transformers import TextIteratorStreamer
    from threading import Thread
    import json
    
    app = FastAPI()
    
    @app.post("/v1/chat/completions")
    async def chat_stream(request: ChatRequest):
        
        # Setup streamer
        streamer = TextIteratorStreamer(tokenizer)
        thread = Thread(target=model.generate, kwargs={
            **inputs, "streamer": streamer
        })
        
        async def generate():
            thread.start()
            for token in streamer:
                # Format SSE (mirip OpenAI)
                data = {
                    "choices": [{
                        "delta": {"content": token},
                        "finish_reason": None
                    }]
                }
                yield f"data: {json.dumps(data)}\\n\\n"
            
            # Signal selesai
            yield "data: [DONE]\\n\\n"
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream"
        )
    ```

    2. Client-side (JavaScript):
    
    ```javascript
    const response = await fetch('/v1/chat/completions', {
        method: 'POST',
        body: JSON.stringify({ messages: [...] }),
        headers: { 'Content-Type': 'application/json' }
    });
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    
    while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        
        const chunk = decoder.decode(value);
        const data = JSON.parse(chunk.replace('data: ', ''));
        document.getElementById('output').innerText += 
            data.choices[0].delta.content;
    }
    ```
    """)


def main():
    demo_non_streaming()
    demo_streaming_textstreamer()
    demo_custom_streamer()
    demo_sse_pattern()

    print("\n" + "=" * 60)
    print("✅ Selesai! Lanjut ke: 05_inference_api_dan_serving/")
    print("=" * 60)

if __name__ == "__main__":
    main()
