import os
import sys
import subprocess

def run_script(script_path):
    print(f"\n{'='*50}")
    print(f"Menjalankan: {os.path.basename(os.path.dirname(script_path))}/{os.path.basename(script_path)}")
    print(f"{'='*50}")
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"\n[ERROR] Gagal menjalankan skrip: {e}")
    except FileNotFoundError:
        print(f"\n[ERROR] File tidak ditemukan: {script_path}")
    print(f"{'='*50}\n")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    while True:
        print("\n" + "#"*60)
        print("=== AI Agents Learning Project (roadmap.sh) ===")
        print("#"*60)
        print("Pilih modul / point yang ingin Anda jalankan:\n")

        print("[ Point 1: LLM Fundamentals (Fondasi - 'Otak' Agent) ]")
        print("  11. API Call (OpenAI-Compatible)")
        print("  12. Generation Controls (Temperature, Top-P, Max Tokens)")
        print("  13. Tokenization & Context Window  ** tanpa API key")

        print("\n[ Point 2: Prompt Engineering ]")
        print("  21. Basic Prompting (System/User/Assistant Roles)")
        print("  22. Chain-of-Thought (CoT) Prompting")
        print("  23. Structured Output (JSON)")

        print("\n[ Point 3: Tools & Function Calling ]")
        print("  31. Function Calling - Dasar")
        print("  32. Tool Execution (Eksekusi Lengkap)")
        print("  33. Multi-Tool Agent")

        print("\n[ Point 4: Agent Loop ]")
        print("  41. ReAct Agent Manual (Thought/Action/Observation)")
        print("  42. Agent Loop dengan Function Calling")

        print("\n[ Point 5: Memory ]")
        print("  51. Conversation Memory (Short-Term)")
        print("  52. Summary Memory (Ringkasan)")
        print("  53. Vector Memory (Long-Term)  ** tanpa API key")

        print("\n[ Point 6: RAG (Retrieval-Augmented Generation) ]")
        print("  61. Embedding & Cosine Similarity  ** tanpa API key")
        print("  62. Simple RAG Pipeline")
        print("  63. RAG dengan Chunking")

        print("\n[ Point 7: Multi-Agent Systems ]")
        print("  71. Sequential Agents (Pipeline)")
        print("  72. Supervisor Agent (Delegasi)")

        print("\n[ Point 8: Guardrails & Safety ]")
        print("  81. Input Validation (Deteksi Prompt Injection)")
        print("  82. Output Guardrails (PII, Safety Check)")

        print("\n[ Point 9: Evaluasi & Observability ]")
        print("  91. Evaluasi Agent (LLM-as-Judge)")
        print("  92. Logging & Tracing  ** tanpa API key")

        print("\n  0. Keluar")

        pilihan = input("\nMasukkan angka pilihan Anda: ").strip()

        # Mapping input ke path file
        scripts_map = {
            '11': "01_llm_fundamentals/1_api_call_openai_compatible.py",
            '12': "01_llm_fundamentals/2_generation_controls.py",
            '13': "01_llm_fundamentals/3_tokenization_dan_context.py",
            '21': "02_prompt_engineering/1_basic_prompting.py",
            '22': "02_prompt_engineering/2_chain_of_thought.py",
            '23': "02_prompt_engineering/3_structured_output.py",
            '31': "03_tools_dan_function_calling/1_function_calling_basic.py",
            '32': "03_tools_dan_function_calling/2_tool_execution.py",
            '33': "03_tools_dan_function_calling/3_multi_tool_agent.py",
            '41': "04_agent_loop/1_react_agent_manual.py",
            '42': "04_agent_loop/2_agent_loop_with_tools.py",
            '51': "05_memory/1_conversation_memory.py",
            '52': "05_memory/2_summary_memory.py",
            '53': "05_memory/3_vector_memory.py",
            '61': "06_rag/1_embedding_dan_similarity.py",
            '62': "06_rag/2_simple_rag_pipeline.py",
            '63': "06_rag/3_rag_with_chunking.py",
            '71': "07_multi_agent/1_sequential_agents.py",
            '72': "07_multi_agent/2_supervisor_agent.py",
            '81': "08_guardrails_dan_safety/1_input_validation.py",
            '82': "08_guardrails_dan_safety/2_output_guardrails.py",
            '91': "09_evaluasi_dan_observability/1_basic_evaluation.py",
            '92': "09_evaluasi_dan_observability/2_logging_dan_tracing.py",
        }

        if pilihan == '0':
            print("Keluar dari program. Terima kasih!")
            break
        elif pilihan in scripts_map:
            script_path = os.path.join(base_dir, scripts_map[pilihan])
            run_script(script_path)
        else:
            print("[PERINGATAN] Pilihan tidak valid. Silakan masukkan angka yang tersedia (misal: 11, 21, 31).")

if __name__ == "__main__":
    main()
