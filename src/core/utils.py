"""Utility functions for file and JSON handling."""

import json
from pathlib import Path
from typing import List, Dict
import logging
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def pick_requirement(file_path: str = None, req_dir: str = "data/requirements") -> Path:
    """Select requirement file - either specific path or first .txt in directory."""

    # If specific file given, use it
    if file_path:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        return path

    # Otherwise, pick first .txt file
    txt_files = sorted(Path(req_dir).glob("*.txt"))
    if not txt_files:
        raise FileNotFoundError(f"No .txt files found in {req_dir}")

    return txt_files[0]

def get_logger(name: str) -> logging.Logger:
    """Create and configure a logger."""
    logger = logging.getLogger(name)

    # Get log level from .env (default: INFO)
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, log_level, logging.INFO)
    logger.setLevel(level)

    # Avoid duplicate handlers
    if logger.handlers:
        return logger

    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    # Format: [INFO] Agent started
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger

def print_summary(duration: float, metadata: dict, llm_calls:int=1, status: str = "Success"):
    """Print performance summary."""
    print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("📊 Performance Summary")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"⏱️  Duration:       {duration:.2f}s")
    print(f"🤖 LLM Calls:      {llm_calls}")
    print(f"📝 Total Tokens:   {metadata['total_tokens']}")
    print(f"💰 Cost:           ${metadata['cost_usd']:.6f}")
    print(f"🔧 Provider:       {metadata['provider']}/{metadata['model']}")
    print(f"✅ Status:         {status}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")