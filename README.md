An AI-powered test case generator that reads software requirements and automatically produces structured test cases using LangChain and your choice of LLM provider (OpenAI, Google Gemini, or Ollama).

📁 Project Structure
Langchain_Agent_TestCaseGenerator/
├── data/
│   └── requirements/           # Input requirement files (.txt)
│       ├── api_user_registration.txt
│       └── payment_checkout.txt
├── outputs/
│   └── testcase_generated/     # Generated outputs
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
├── .env                            # Environment configuration (not committed)
├── .gitignore
└── requirements.txt

✨ Features

Multi-provider support — Switch between OpenAI, Google Gemini, or local Ollama models via .env
LangChain LCEL pipeline — Uses ChatPromptTemplate | LLM | JsonOutputParser
Structured JSON output — Test cases with id, title, steps, expected, priority, tags, and likelihood
CSV export — Ready-to-import test case spreadsheet
Token tracking — Logs prompt/completion tokens and estimated cost per run
Performance summary — Prints duration, token usage, and cost after each run
A summary is also printed to the console:
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
