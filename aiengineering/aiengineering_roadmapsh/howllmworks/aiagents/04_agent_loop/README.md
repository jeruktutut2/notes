# Implementasi Point 4: Agent Loop (Siklus Agent)

Modul ini berisi implementasi inti dari AI Agent: sebuah loop di mana agent
menerima input → berpikir → bertindak → mengamati → ulangi.

## Konsep Utama
- **ReAct Pattern**: Reasoning + Acting — agent berpikir (Thought), memilih aksi (Action),
  mendapat hasil (Observation), lalu berpikir lagi sampai tugas selesai.
- **Agent Loop**: While loop yang terus berputar sampai agent memutuskan untuk berhenti.

## Daftar File
1. `1_react_agent_manual.py`: Implementasi ReAct pattern dengan format Thought/Action/Observation secara manual.
2. `2_agent_loop_with_tools.py`: Agent loop lengkap dengan function calling dan multiple tools.

## Urutan Eksekusi

```bash
python 1_react_agent_manual.py
python 2_agent_loop_with_tools.py
```

### Cara Instalasi Library
```bash
pip install openai
```
