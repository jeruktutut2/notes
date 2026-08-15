# 01. 14 Gold Rules of Prompting Best Practices

## Overview
Dokumen ini mendokumentasikan **14 Aturan Emas Prompting Best Practices** yang tercantum pada kotak utama diagram [roadmap.sh/prompt-engineering](https://roadmap.sh/prompt-engineering).

---

## Daftar 14 Aturan Emas Best Practices

1. **Provide few-shot examples for structure or output style you need**  
   *Berikan contoh few-shot untuk menegaskan struktur atau gaya output yang Anda butuhkan.*

2. **Keep your prompts short and concise**  
   *Jaga agar prompt tetap ringkas, padat, dan langsung ke inti masalah tanpa kata-kata tak berguna.*

3. **Ask for structured output if it helps e.g. JSON, XML, Markdown, CSV etc**  
   *Minta format terstruktur seperti JSON, XML, Markdown, atau CSV agar respons mudah diparse oleh software.*

4. **Use variables / placeholders in your prompts for easier configuration**  
   *Gunakan variabel/placeholder seperti `{{user_query}}` atau `{document_text}` agar prompt reusable.*

5. **Prioritize giving clearer instructions over adding constraints**  
   *Utamakan memberikan instruksi positif yang jelas daripada menumpuk banyak larangan/batasan.*

6. **Control the maximum output length**  
   *Kendalikan panjang output maksimum menggunakan `max_tokens` atau instruksi pembatas kata.*

7. **Experiment with input formats and writing styles**  
   *Lakukan eksperimen dengan variasi format input dan gaya penulisan untuk menemukan performa terbaik.*

8. **Tune sampling (temperature, top-k, top-p) for determinism vs creativity**  
   *Sesuaikan parameter sampling (Temperature 0.0 untuk fakta/kode, 0.7+ untuk kreativitas).*

9. **Guard against prompt injection; sanitize user text**  
   *Lindungi model dari Prompt Injection; lakukan pembersihan dan sanitasi pada teks input pengguna.*

10. **Automate evaluation; integrate unit tests for outputs**  
    *Otomatiskan evaluasi; integrasikan unit test untuk menguji validitas output LLM secara berskala.*

11. **Document and track prompt versions**  
    *Dokumentasikan dan lacak versi prompt (Prompt Version Control: v1.0, v1.1) layaknya kode program.*

12. **Optimize for latency & cost in production pipelines**  
    *Optimalkan latensi dan biaya pada pipeline produksi (kompresi prompt, caching, pemangkasan token).*

13. **Document decisions, failures, and learnings for future devs**  
    *Dokumentasikan keputusan, kegagalan, dan temuan penting untuk developer lain di tim Anda.*

14. **Delimit different sections with triple backticks or XML tags**  
    *Pisahkan setiap bagian prompt menggunakan delimiter jelas seperti ``` atau tag XML `<context>...`.*
