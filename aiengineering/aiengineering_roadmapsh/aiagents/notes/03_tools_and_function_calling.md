# 03. Tools & Function Calling

**Tools & Function Calling** adalah kemampuan LLM native untuk mengenali definisi fungsi (nama, deskripsi, dan skema parameter JSON) dan menghasilkan output terstruktur (Structured Tool Calls) yang dapat dieksekusi oleh runtime program secara aman.

---

## 1. Mengapa Native Function Calling Lebih Bagus dari String Parsing?

Dahulu (seperti pada ReAct berbasis prompt murni), LLM mengeluarkan teks mentah seperti `Action: search("Jakarta")`. Karakteristik ini rentan error parsing (misalnya tanda kurung salah, kutipan tidak tertutup, atau format JSON rusak).

Dengan **Native Function Calling** (yang didukung oleh OpenAI, Claude, Gemini, dll):
1. **Penyempurnaan Syntax**: LLM dilatih secara khusus untuk mengeluarkan JSON skema yang valid.
2. **Type Safety**: Parameter divalidasi berdasarkan tipe data (`string`, `integer`, `boolean`, `array`, `object`).
3. **Multi-Tool Calling**: LLM dapat memilih beberapa tools sekaligus dalam satu turn.

---

## 2. Siklus Alur Function Calling (The Tool Call Lifecycle)

```
+---------------+                +---------------+               +-----------------+
|   App / Code  |                |   LLM Model   |               | Target Function |
+---------------+                +---------------+               +-----------------+
        |                                |                                |
        |--- Send Prompt & Tools Schema ->|                                |
        |                                |-- (Decides to call tool)       |
        |<-- Return Tool Call Request ----|                                |
        |    (func_name, JSON args)      |                                |
        |                                                                 |
        |------------------- Execute Local Function --------------------->|
        |<------------------ Return Execution Result ---------------------|
        |                                                                 |
        |--- Send Execution Result ----->|                                |
        |    (tool_call_id + payload)    |                                |
        |                                |-- Generates Final Response --> |
        |<-- Return Final Response ------|                                |
```

---

## 3. Cara Mendefinisikan Tool Schema (Standard JSON Schema)

### Format JSON Schema (OpenAI / Generic Standard):
```json
{
  "type": "function",
  "function": {
    "name": "get_stock_price",
    "description": "Mengambil harga saham terkini berdasarkan ticker simbol.",
    "parameters": {
      "type": "object",
      "properties": {
        "ticker": {
          "type": "string",
          "description": "Simbol kode saham, contoh: AAPL, TSLA, BBCA.JK"
        },
        "currency": {
          "type": "string",
          "enum": ["USD", "IDR"],
          "description": "Mata uang hasil harga."
        }
      },
      "required": ["ticker"]
    }
  }
}
```

### Menggunakan Pydantic (Python Tool Registration):
```python
from pydantic import BaseModel, Field

class StockQueryInput(BaseModel):
    ticker: str = Field(description="Simbol kode saham, contoh: AAPL, TSLA")
    currency: str = Field(default="USD", description="Mata uang keluaran")

def get_stock_price(ticker: str, currency: str = "USD") -> str:
    # Fungsi aktual yang mengeksekusi API
    return f"Harga {ticker}: 150 {currency}"
```

---

## 4. Aspek Keamanan & Practical Best Practices

1. **Sandboxing & Permission Control**: Jangan pernah membiarkan agent menjalankan command terminal arbitrari atau skrip SQL secara langsung tanpa validasi/ijin pengguna.
2. **Error Handling & Feedback**: Jika fungsi lokal menghasilkan *Exception* (misal: API Timeout atau 404), kembalikan pesan error tersebut ke LLM sebagai `Observation`/`Tool Output` agar agen bisa menyesuaikan aksinya.
3. **Idempotency**: Pastikan alat yang memiliki efek samping besar (seperti `send_email` atau `delete_database`) dikonfirmasi terlebih dahulu (*Human-in-the-Loop*).
