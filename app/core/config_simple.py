"""
Simplified configuration that doesn't depend on pydantic_settings
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Project Settings
PROJECT_NAME = "AI-Powered GitHub Auto-Manager"
VERSION = "1.0.0"
API_V1_STR = "/api/v1"

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini"

# GitHub Configuration
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "")
GITHUB_DEFAULT_BRANCH = "main"
GITHUB_ANALYSIS_TIMEOUT = 300  # seconds

# Web Automation Settings
PLAYWRIGHT_BROWSER = "chromium"
PLAYWRIGHT_TIMEOUT = 30000

# Model Management Settings
DEFAULT_MODEL_CONFIG = {
    "code_analysis": {
        "model_type": "gpt-4o-mini",
        "temperature": 0.7,
        "max_tokens": 2000,
        "context_window": 8000
    },
    "bug_detection": {
        "model_type": "gpt-4o-mini",
        "temperature": 0.3,
        "max_tokens": 1000,
        "context_window": 4000
    },
    "code_refactoring": {
        "model_type": "gpt-4o-mini",
        "temperature": 0.5,
        "max_tokens": 1500,
        "context_window": 6000
    },
    "issue_analysis": {
        "model_type": "gpt-4o-mini",
        "temperature": 0.7,
        "max_tokens": 1000,
        "context_window": 4000
    },
    "pr_review": {
        "model_type": "gpt-4o-mini",
        "temperature": 0.5,
        "max_tokens": 1500,
        "context_window": 6000
    }
} 