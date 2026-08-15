"""
MODUL 3.1: ReAct (Reasoning + Acting) Framework
===============================================
Penjelasan:
ReAct menggabungkan penalaran (Thought) dan aksi (Action/Tool Call) secara interaktif.
Siklus ReAct:
1. Thought: LLM memikirkan langkah berikutnya.
2. Action: LLM memilih tool yang akan dipanggil (misal: Search, Calculator, DB Query).
3. Observation: Hasil dari eksekusi tool dikembalikan ke LLM.
4. Ulangi hingga menemukan Final Answer.
"""

import json

def mock_tool_calculator(expression: str) -> str:
    """Tool simulasi kalkulator."""
    try:
        # kalkulasi aman sederhana
        val = eval(expression, {"__builtins__": None}, {})
        return str(val)
    except Exception as e:
        return f"Error kalkulasi: {e}"


def mock_tool_search(query: str) -> str:
    """Tool simulasi pencarian database/internet."""
    db = {
        "populasi jakarta 2024": "10.67 juta jiwa",
        "harga emas hari ini": "Rp 1.350.000 per gram",
        "jarak jakarta bandung": "150 km"
    }
    query_lower = query.lower()
    for k, v in db.items():
        if k in query_lower:
            return v
    return "Data tidak ditemukan."


def run_react_agent(user_query: str):
    print(f"User Query: '{user_query}'\n")
    
    # Step 1
    print("--- Iterasi 1 ---")
    thought1 = "Saya perlu mencari populasi Jakarta tahun 2024 terlebih dahulu."
    action1 = {"tool": "search", "query": "populasi jakarta 2024"}
    print(f"Thought 1: {thought1}")
    print(f"Action 1: {json.dumps(action1)}")
    
    obs1 = mock_tool_search(action1["query"])
    print(f"Observation 1: {obs1}\n")
    
    # Step 2
    print("--- Iterasi 2 ---")
    thought2 = "Populasi Jakarta 10.67 juta jiwa. Jika setiap jiwa membutuhkan 2 liter air per hari, saya perlu menghitung 10.67 * 2."
    action2 = {"tool": "calculator", "expression": "10.67 * 2"}
    print(f"Thought 2: {thought2}")
    print(f"Action 2: {json.dumps(action2)}")
    
    obs2 = mock_tool_calculator(action2["expression"])
    print(f"Observation 2: {obs2} juta liter\n")
    
    # Step 3
    print("--- Iterasi 3 ---")
    thought3 = "Saya telah memiliki semua informasi yang dibutuhkan."
    final_answer = f"Berdasarkan data populasi Jakarta 2024 ({obs1}), total estimasi kebutuhan air harian adalah {obs2} juta liter per hari."
    print(f"Thought 3: {thought3}")
    print(f"Final Answer: {final_answer}")


def main():
    print("==========================================================")
    print(" DEMO 3.1: ReAct Framework (Thought -> Action -> Observation)")
    print("==========================================================\n")

    user_query = "Berapa total kebutuhan air harian di Jakarta jika tiap orang butuh 2 liter/hari?"
    run_react_agent(user_query)
    print("==========================================================")

if __name__ == "__main__":
    main()
