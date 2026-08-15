# AI Safety and Ethics Learning Workspace

Welcome to the **AI Safety and Ethics** interactive learning module! This repository is modeled after the [roadmap.sh AI Engineer path](https://roadmap.sh/ai-engineer) and structured with technical notes, hands-on executable Python labs, a master CLI runner, and an interactive Web Visualizer.

---

## 🎯 Learning Objectives & Roadmap Overview

This module covers the two core pillars of Generative AI Security & Ethics:

```
+-----------------------------------------------------------------------------------+
|                            AI SAFETY & ETHICS ROADMAP                             |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|  [Module 01: Understanding AI Safety Issues]                                      |
|   ├── Prompt Injection Attacks (Direct, Indirect, Jailbreak, System Leakage)       |
|   ├── Security and Privacy Concerns (PII Redaction, Insecure Outputs, DLP)         |
|   └── Bias and Fairness (Demographic Disparity, Counterfactual Audits)            |
|                                                                                   |
|  [Module 02: Safety Best Practices]                                              |
|   ├── Content Moderation APIs (Pre & Post Filters, Category Scoring)               |
|   ├── Adding end-user IDs in prompts (Session tracking, Rate limiting)             |
|   ├── Conducting adversarial testing (Red Teaming, Automated Attack Suites)       |
|   ├── Robust prompt engineering (XML Delimiters, Instruction Sandwiching)          |
|   ├── Know your Customers / Usecases (KYC, Domain Scoping, Human-in-the-Loop)      |
|   └── Constraining outputs and inputs (Input Caps, Pydantic Schema Enforcement)    |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 📁 Repository Structure

```
aisafetyandetichs/
├── README.md                           # Main documentation & course guide
├── requirements.txt                    # Project dependencies
├── main.py                             # Master CLI runner for interactive labs
├── notes/                              # Comprehensive technical manuals
│   ├── 01_understanding_ai_safety_issues.md
│   └── 02_safety_best_practices.md
├── 01_understanding_safety_issues/
│   ├── 01_prompt_injection.py          # Direct/Indirect Injection & Delimiter Defenses
│   ├── 02_security_privacy.py          # PII Redaction & Insecure Output Checks
│   └── 03_bias_fairness.py             # Disparate Impact & Counterfactual Auditing
├── 02_safety_best_practices/
│   ├── 01_content_moderation.py        # Automated Moderation Pipelines
│   ├── 02_user_id_tracking.py          # User Context Tracking & Threat Scoring
│   ├── 03_adversarial_testing.py       # Automated Red-Teaming Test Harness
│   ├── 04_robust_prompt_engineering.py # XML Isolation & Instruction Precedence
│   ├── 05_kyc_and_usecase_boundaries.py# Domain Scoping & HITL Triggers
│   └── 06_constraining_inputs_outputs.py# Input Caps & Pydantic Structured Output
└── web_visualizer/                      # Interactive Web GUI & API Server
    ├── index.html                      # Visual Dashboard & Simulator UI
    ├── styles.css                      # Modern dark-mode styling & layout
    ├── app.js                          # Interactive logic & simulation engine
    └── server.py                       # FastAPI HTTP & API Backend
```

---

## 🚀 Quickstart Guide

### 1. Installation
Install project dependencies:
```bash
pip install -r requirements.txt
```

### 2. Running Interactive Python Labs via CLI
Run the master CLI runner to select and execute any safety lab:
```bash
python main.py
```

Or run individual lab scripts directly:
```bash
python 01_understanding_safety_issues/01_prompt_injection.py
python 02_safety_best_practices/03_adversarial_testing.py
```

### 3. Launching the Web Visualizer
Start the Python FastAPI server to open the interactive dashboard:
```bash
python web_visualizer/server.py
```
Then open `http://localhost:8000` in your web browser!
