"""
TestCase Generator Agent - Langchain Version
Generates test cases from requirements using Langchain.
"""
import sys
from datetime import time
from time import time
from pathlib import Path

# Langchain imports
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

# Our core utilities
from src.core import get_langchain_llm, pick_requirement, get_logger, TokenTrackingCallback, print_summary,  PROVIDER, MODEL

# Import prompt
from src.prompts.testcase_prompts import TESTCASE_SYSTEM_PROMPT

# Project paths
ROOT = Path(__file__).resolve().parents[2]
REQ_DIR = ROOT / "data" / "requirements"
OUT_DIR = ROOT / "outputs" / "testcase_generated"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Logger
logger = get_logger("testcase_langchain")

# Get LLM
llm = get_langchain_llm()

# Get Parser
parser = JsonOutputParser()

prompt_template = ChatPromptTemplate.from_messages([
    ("system", TESTCASE_SYSTEM_PROMPT),
    ("user", "Requirements: \n\n{requirement}")
])


# Build Chain using LECL (Pipe operatpr)
chain = prompt_template | llm | parser

def main():
    logger.info("TestCase Agent (Langchain) started")

    # 1. Pick requirement file
    file_arg = sys.argv[1] if len(sys.argv) > 1 else None
    req_file = pick_requirement(file_arg, REQ_DIR)
    requirement = req_file.read_text(encoding="utf-8")
    logger.info(f"Processing: {req_file.name}")

    # 2. Setup callback + LLM + chain
    tracker = TokenTrackingCallback()                     # <-- create tracker
    llm = get_langchain_llm(callbacks=[tracker])          # <-- pass tracker to LLM

    chain = prompt_template | llm | parser

    # 3. Run chain with timing
    # 3. Run chain with timing
    logger.info("Calling LLM via Langchain...")
    start_time = time()

    # Step 1: call LLM directly to capture response metadata
    formatted_prompt = prompt_template.format_messages(requirement=requirement)
    llm_response = llm.invoke(formatted_prompt)

    # Step 2: parse separately
    testcases = parser.parse(llm_response.content)

    duration = time() - start_time

    # Step 3: read token usage directly from response
    usage = llm_response.usage_metadata or {}
    prompt_tokens = usage.get("input_tokens", 0)
    output_tokens = usage.get("output_tokens", 0)
    total_tokens = usage.get("total_tokens", prompt_tokens + output_tokens)

    # 4. Save outputs (your existing code, unchanged)
    import json
    import pandas as pd

    raw_file = OUT_DIR / "raw_output_langchain.txt"
    raw_file.write_text(json.dumps(testcases, indent=2), encoding="utf-8")

    csv_file = OUT_DIR / "test_cases_langchain.csv"
    df = pd.DataFrame(testcases)
    df['steps'] = df['steps'].apply(lambda x: ' | '.join(x))
    df.to_csv(csv_file, index=False)

    # 5. Log results
    logger.info(f"Generated {len(testcases)} test cases")
    logger.info(f"Raw JSON: {raw_file.relative_to(ROOT)}")
    logger.info(f"CSV: {csv_file.relative_to(ROOT)}")

    # 6. Build metadata and print summary
    from src.core.cost_tracker import calculate_cost
    cost = calculate_cost(PROVIDER, MODEL, prompt_tokens, output_tokens)

    metadata = {
        "total_tokens": total_tokens,
        "cost_usd": cost,
        "provider": PROVIDER,
        "model": MODEL
    }

    print_summary(duration=duration, metadata=metadata, llm_calls=1, status="Success")

    logger.info("TestCase Agent (Langchain) completed")

if __name__ == "__main__":
    main()