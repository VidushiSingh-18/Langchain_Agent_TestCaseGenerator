import os
from time import time

from dotenv import load_dotenv
from pathlib import Path
from typing import List, Dict

from openai import OpenAI
from google import genai
from ollama import Client as OllamaClient
from .cost_tracker import calculate_cost

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import Ollama
from langchain_core.callbacks.base import BaseCallbackHandler

# Load .env from project root (works regardless of cwd)
load_dotenv(Path(__file__).resolve().parents[2] / ".env")

# Read configuration from .env file
PROVIDER = os.getenv("PROVIDER", "openai").lower()
MODEL = os.getenv("MODEL", "gpt-4o-mini")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
TIMEOUT = 60

Message = Dict[str, str]


class TokenTrackingCallback(BaseCallbackHandler):
    """Tracks token usage and cost from LLM responses."""

    def __init__(self):
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.total_tokens = 0

    def on_llm_end(self, response, **kwargs):
        """Called automatically by LangChain after every LLM call."""
        usage = response.llm_output.get("token_usage") or response.llm_output.get("usage_metadata", {})
        self.prompt_tokens += usage.get("prompt_tokens", 0)
        self.completion_tokens += usage.get("completion_tokens", 0)
        self.total_tokens += usage.get("total_tokens", 0)

    def on_llm_start(self, serialized, prompts, **kwargs):
        print("DEBUG: on_llm_start fired")

    def on_llm_end(self, response, **kwargs):
        print("DEBUG: on_llm_end fired")
        print("DEBUG llm_output:", response.llm_output)

    from src.core.cost_tracker import calculate_cost
    def get_metadata(self) -> dict:
        """Returns metadata dict expected by print_summary."""
        cost = calculate_cost(PROVIDER, MODEL, prompt_tokens, output_tokens)

        metadata = {
            "total_tokens": total_tokens,
            "cost_usd": cost,
            "provider": PROVIDER,
            "model": MODEL
        }
def get_langchain_llm(callbacks = None):
    if PROVIDER == "openai":
        return ChatOpenAI(
            model=MODEL,
            temperature=0,
            api_key=OPENAI_API_KEY,
            callbacks = callbacks
        )

    elif PROVIDER == "google":
        return ChatGoogleGenerativeAI(
            model=MODEL,
            temperature=0,
            google_api_key=GOOGLE_API_KEY,
            callbacks=callbacks
        )

    elif PROVIDER == "ollama":
        return Ollama(
            model=MODEL,
            temperature=0,
            base_url=OLLAMA_HOST,
            callbacks=callbacks
        )

    else:
        raise ValueError(f"Unsupported provider: {PROVIDER}")