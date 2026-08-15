# Prompt Engineering Learning Workspace

Peta jalan pembelajaran **Prompt Engineering** komprehensif dan interaktif yang disusun 100% berdasarkan kurikulum resmi [roadmap.sh/prompt-engineering](https://roadmap.sh/prompt-engineering).

---

## 🗺️ Peta Navigasi Kurikulum (Roadmap Nodes Mapping)

```
                                  ┌──────────────────────────────┐
                                  │         Introduction         │
                                  └──────────────┬───────────────┘
                                                 │
          ┌──────────────────────────────────────┼──────────────────────────────────────┐
          │                                      │                                      │
┌─────────▼──────────┐                 ┌─────────▼──────────┐                 ┌─────────▼──────────┐
│ Common Terminology │                 │ LLM Configuration  │                 │ Major Providers    │
│ • LLM              │                 │ • Temperature      │                 │ • OpenAI           │
│ • Tokens           │                 │ • Top-K / Top-P    │                 │ • Google           │
│ • Context Window   │                 │ • Max Tokens       │                 │ • Anthropic        │
│ • Hallucination    │                 │ • Stop Sequences   │                 │ • Meta             │
│ • Agents           │                 │ • Penalties        │                 │ • xAI              │
│ • Prompt Injection │                 └─────────┬──────────┘                 └────────────────────┘
│ • Model Weights    │                           │
│ • Fine-Tuning      │                           │
│ • AI vs AGI        │                 ┌─────────▼──────────┐
│ • RAG              │                 │ Prompting          │
└────────────────────┘                 │ Techniques         │
                                       │ • Zero/Few-Shot    │
                                       │ • System/Role      │
                                       │ • Step-back        │
                                       │ • CoT & ToT        │
                                       │ • ReAct            │
                                       └─────────┬──────────┘
                                                 │
          ┌──────────────────────────────────────┼──────────────────────────────────────┐
          │                                      │                                      │
┌─────────▼──────────┐                 ┌─────────▼──────────┐                 ┌─────────▼──────────┐
│ Structured Outputs │                 │ 14 Best Practices  │                 │ Improving          │
│ & Auto Prompts     │                 │ & AI Red Teaming   │                 │ Reliability        │
│ • JSON / XML       │                 │ • Delimiters       │                 │ • Debiasing        │
│ • APE Generator    │                 │ • Placeholders     │                 │ • Ensembling       │
│ • Meta-Prompting   │                 │ • Sanitization     │                 │ • Self Evaluation  │
└────────────────────┘                 └────────────────────┘                 └────────────────────┘
```

---

## 📁 Struktur Modul & Dokumen Catatan

### [Modul 01: Introduction & Terminology](file:///Users/bsa/Documents/por/promptengineering/01_introduction_and_terminology/README.md)
- 📝 [01_llm_mechanics_and_prompts.md](file:///Users/bsa/Documents/por/promptengineering/01_introduction_and_terminology/notes/01_llm_mechanics_and_prompts.md) — LLMs & how they work, What is a Prompt, What is Prompt Engineering.
- 📝 [02_common_terminology.md](file:///Users/bsa/Documents/por/promptengineering/01_introduction_and_terminology/notes/02_common_terminology.md) — LLM, Tokens, Context Window, Hallucination, Agents, Prompt Injection, Model Weights, Fine-Tuning, AI vs AGI, RAG.
- 📝 [03_model_providers.md](file:///Users/bsa/Documents/por/promptengineering/01_introduction_and_terminology/notes/03_model_providers.md) — OpenAI, Google, Anthropic, Meta, xAI.
- 💻 [token_context_calculator.py](file:///Users/bsa/Documents/por/promptengineering/01_introduction_and_terminology/code/token_context_calculator.py)

### [Modul 02: LLM Configuration](file:///Users/bsa/Documents/por/promptengineering/02_llm_configuration/README.md)
- 📝 [01_sampling_parameters.md](file:///Users/bsa/Documents/por/promptengineering/02_llm_configuration/notes/01_sampling_parameters.md) — Temperature, Top-K, Top-P.
- 📝 [02_output_control_and_penalties.md](file:///Users/bsa/Documents/por/promptengineering/02_llm_configuration/notes/02_output_control_and_penalties.md) — Max Tokens, Stop Sequences, Frequency Penalty, Presence Penalty.
- 💻 [hyperparameters_experiment.py](file:///Users/bsa/Documents/por/promptengineering/02_llm_configuration/code/hyperparameters_experiment.py)

### [Modul 03: Prompting Techniques](file:///Users/bsa/Documents/por/promptengineering/03_prompting_techniques/README.md)
- 📝 [01_basic_and_role_prompting.md](file:///Users/bsa/Documents/por/promptengineering/03_prompting_techniques/notes/01_basic_and_role_prompting.md) — Zero-Shot, One-Shot / Few-Shot, System, Role, Contextual.
- 📝 [02_advanced_reasoning_prompts.md](file:///Users/bsa/Documents/por/promptengineering/03_prompting_techniques/notes/02_advanced_reasoning_prompts.md) — Step-back, CoT, Self-Consistency, ToT, ReAct, Prompt Tuning.
- 💻 [zero_few_shot_demo.py](file:///Users/bsa/Documents/por/promptengineering/03_prompting_techniques/code/zero_few_shot_demo.py)
- 💻 [cot_tot_react_solver.py](file:///Users/bsa/Documents/por/promptengineering/03_prompting_techniques/code/cot_tot_react_solver.py)

### [Modul 04: Structured Outputs & Auto Prompts](file:///Users/bsa/Documents/por/promptengineering/04_structured_outputs_and_auto_prompts/README.md)
- 📝 [01_structured_outputs.md](file:///Users/bsa/Documents/por/promptengineering/04_structured_outputs_and_auto_prompts/notes/01_structured_outputs.md) — JSON, XML, Markdown, CSV, Schema Enforcement.
- 📝 [02_automatic_prompt_engineering.md](file:///Users/bsa/Documents/por/promptengineering/04_structured_outputs_and_auto_prompts/notes/02_automatic_prompt_engineering.md) — APE, Meta-Prompting.
- 💻 [structured_output_enforcer.py](file:///Users/bsa/Documents/por/promptengineering/04_structured_outputs_and_auto_prompts/code/structured_output_enforcer.py)
- 💻 [auto_prompt_generator.py](file:///Users/bsa/Documents/por/promptengineering/04_structured_outputs_and_auto_prompts/code/auto_prompt_generator.py)

### [Modul 05: Best Practices & Red Teaming](file:///Users/bsa/Documents/por/promptengineering/05_best_practices_and_red_teaming/README.md)
- 📝 [01_prompting_best_practices.md](file:///Users/bsa/Documents/por/promptengineering/05_best_practices_and_red_teaming/notes/01_prompting_best_practices.md) — 14 Aturan Emas Best Practices.
- 📝 [02_ai_red_teaming.md](file:///Users/bsa/Documents/por/promptengineering/05_best_practices_and_red_teaming/notes/02_ai_red_teaming.md) — Prompt Injection, Jailbreaking, Sanitization.
- 💻 [best_practices_auditor.py](file:///Users/bsa/Documents/por/promptengineering/05_best_practices_and_red_teaming/code/best_practices_auditor.py)
- 💻 [red_teaming_simulator.py](file:///Users/bsa/Documents/por/promptengineering/05_best_practices_and_red_teaming/code/red_teaming_simulator.py)

### [Modul 06: Improving Reliability](file:///Users/bsa/Documents/por/promptengineering/06_improving_reliability/README.md)
- 📝 [01_reliability_techniques.md](file:///Users/bsa/Documents/por/promptengineering/06_improving_reliability/notes/01_reliability_techniques.md) — Debiasing, Ensembling, LLM Self Evaluation, Calibration.
- 💻 [reliability_suite.py](file:///Users/bsa/Documents/por/promptengineering/06_improving_reliability/code/reliability_suite.py)

---

## ⚡ Panduan Menjalankan Kode & Web Visualizer Studio

### 1. Menjalankan Interactive CLI Launcher
```bash
python3 main.py
```

### 2. Menjalankan Web Visualizer Studio (Port 8080)
```bash
python3 -m http.server 8080 --directory web_visualizer
```
Buka browser Anda di `http://localhost:8080` untuk menikmati Peta Jalan Interaktif, Sandbox Parameter Sampling, Tree of Thoughts Explorer, AI Red Teaming Lab, dan Automated 14 Best Practices Auditor!
