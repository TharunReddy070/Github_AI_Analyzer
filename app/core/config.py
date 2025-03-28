from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Project Settings
    PROJECT_NAME: str = "AI-Powered GitHub Auto-Manager"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = "gpt-4o-mini"
    
    # GitHub Configuration
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    GITHUB_USERNAME: str = os.getenv("GITHUB_USERNAME", "")
    GITHUB_DEFAULT_BRANCH: str = "main"
    GITHUB_ANALYSIS_TIMEOUT: int = 300  # seconds
    
    # Web Automation Settings
    PLAYWRIGHT_BROWSER: str = "chromium"
    PLAYWRIGHT_TIMEOUT: int = 30000
    
    # Model Management Settings
    DEFAULT_MODEL_CONFIG: dict = {
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
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings() 