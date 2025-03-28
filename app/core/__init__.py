"""
Core modules for GitHub AI Analyzer
"""

# Try to import from regular config, fall back to simplified version
try:
    from .model_manager import ModelManager
    from .config import settings
except ImportError:
    from .model_manager import ModelManager
    from .config_simple import *