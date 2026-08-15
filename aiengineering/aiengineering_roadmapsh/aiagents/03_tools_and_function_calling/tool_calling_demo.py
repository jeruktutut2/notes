"""
03_tools_and_function_calling/tool_calling_demo.py
Demo Native Tools & Function Calling Architecture.
Menunjukkan pembuatan JSON Schema dari fungsi Python dan siklus eksekusi tool call.
"""

import json
from typing import Dict, Any, List
from pydantic import BaseModel, Field
from rich.console import Console
from rich.syntax import Syntax

console = Console()

# 1. Definisi Schema menggunakan Pydantic
class WeatherQuery(BaseModel):
    city: str = Field(description="Nama kota yang ingin dicek cuacanya, contoh: Jakarta, Bandung")
    unit: str = Field(default="celsius", description="Satuan suhu: 'celsius' atau 'fahrenheit'")

class CurrencyConvertQuery(BaseModel):
    amount: float = Field(description="Jumlah uang yang ingin dikonversi")
    from_curr: str = Field(description="Mata uang asal, contoh: USD, EUR")
    to_curr: str = Field(description="Mata uang tujuan, contoh: IDR, JPY")

# 2. Implementation Functions
def get_weather(city: str, unit: str = "celsius") -> str:
    mock_data = {
        "jakarta": {"temp": 32, "condition": "Cerah Berawan"},
        "bandung": {"temp": 24, "condition": "Hujan Ringan"},
        "surabaya": {"temp": 34, "condition": "Cerah"}
    }
    c_lower = city.lower()
    if c_lower in mock_data:
        t = mock_data[c_lower]["temp"]
        cond = mock_data[c_lower]["condition"]
        return f"Cuaca di {city}: {t}°C, {cond}"
    return f"Data cuaca untuk {city} tidak ditemukan."

def convert_currency(amount: float, from_curr: str, to_curr: str) -> str:
    rates = {("USD", "IDR"): 16200, ("EUR", "IDR"): 17500}
    pair = (from_curr.upper(), to_curr.upper())
    if pair in rates:
        result = amount * rates[pair]
        return f"{amount} {from_curr} = Rp {result:,.2f}"
    return f"Kurs konversi {from_curr} ke {to_curr} tidak tersedia."

# 3. Generating JSON Schema format (OpenAI / Tool Calling standard)
def pydantic_to_openai_function(name: str, description: str, model_cls: type[BaseModel]) -> Dict[str, Any]:
    schema = model_cls.model_json_schema()
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": schema.get("properties", {}),
                "required": schema.get("required", [])
            }
        }
    }

def main():
    console.print("[bold blue]=== NATIVE TOOLS & FUNCTION CALLING DEMO ===[/bold blue]\n")

    # Step A: Register Schemas
    weather_schema = pydantic_to_openai_function("get_weather", "Mengambil informasi cuaca kota secara realtime.", WeatherQuery)
    currency_schema = pydantic_to_openai_function("convert_currency", "Mengonversi nilai mata uang asing.", CurrencyConvertQuery)

    tools_spec = [weather_schema, currency_schema]
    
    console.print("[bold yellow]1. Generated OpenAI Tool Schema:[/bold yellow]")
    json_str = json.dumps(tools_spec, indent=2)
    console.print(Syntax(json_str, "json", theme="monokai", line_numbers=True))

    # Step B: Simulasikan Model Respons Tool Call Request
    console.print("\n[bold yellow]2. Simulated LLM Tool Call Request Payload:[/bold yellow]")
    simulated_llm_response = {
        "id": "call_abc123xyz",
        "type": "function",
        "function": {
            "name": "get_weather",
            "arguments": "{\"city\": \"Jakarta\", \"unit\": \"celsius\"}"
        }
    }
    console.print(simulated_llm_response)

    # Step C: Dispatch Function Execution
    console.print("\n[bold yellow]3. Executing Function Dispatcher:[/bold yellow]")
    func_name = simulated_llm_response["function"]["name"]
    func_args = json.loads(simulated_llm_response["function"]["arguments"])

    if func_name == "get_weather":
        output = get_weather(**func_args)
    elif func_name == "convert_currency":
        output = convert_currency(**func_args)
    else:
        output = "Unknown Tool"

    console.print(f"[bold green]Execution Output:[/bold green] {output}")

    # Step D: Structure Tool Result Payload Back to LLM Context
    tool_message_context = {
        "role": "tool",
        "tool_call_id": simulated_llm_response["id"],
        "content": output
    }
    console.print("\n[bold yellow]4. Tool Result Message (Context Injection):[/bold yellow]")
    console.print(tool_message_context)

if __name__ == "__main__":
    main()
