# 🧪 LangChain Agent — TestCase Generator

> An AI-powered test case generator that reads software requirements and automatically produces structured test cases using LangChain and your choice of LLM provider (OpenAI, Google Gemini, or Ollama).

---

## 📁 Project Structure

```plaintext
Langchain_Agent_TestCaseGenerator/
├── data/
│   └── requirements/               # Input requirement files (.txt)
│       ├── api_user_registration.txt
│       └── payment_checkout.txt
├── outputs/
│   └── testcase_generated/         # Generated outputs
│       ├── raw_output_langchain.txt
│       └── test_cases_langchain.csv
├── src/
│   ├── agents/
│   │   └── testcase_langchain.py   # Main agent entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── cost_tracker.py         # Token cost calculation
│   │   ├── llm_client.py           # LLM provider abstraction + callbacks
│   │   └── utils.py                # Logging, file utilities, summary printer
│   └── prompts/
│       └── testcase_prompts.py     # System prompt for test case generation
├── .env                            # Environment config (not committed)
├── .gitignore
└── requirements.txt
```

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔌 Multi-provider | Switch between OpenAI, Google Gemini, or Ollama via `.env` |
| 🔗 LCEL Pipeline | `ChatPromptTemplate \| LLM \| JsonOutputParser` |
| 🗂️ Structured Output | JSON test cases with id, title, steps, priority, tags |
| 📊 CSV Export | Ready-to-import spreadsheet after every run |
| 🪙 Token Tracking | Logs prompt/completion tokens and estimated cost |
| ⏱️ Performance Summary | Prints duration, token count, and cost after each run |

---

### Console summary

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 Performance Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱️  Duration:       4.23s
🤖 LLM Calls:      1
📝 Total Tokens:   842
💰 Cost:           $0.000631
🔧 Provider:       openai/gpt-4o-mini
✅ Status:         Success
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```
