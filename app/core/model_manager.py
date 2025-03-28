from typing import Dict, Any, Optional
import logging
from app.core.config import settings
import streamlit as st

logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self):
        """Initialize the ModelManager with default model configurations."""
        self.models = {
            "code_analysis": {
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                "max_tokens": 4000,
                "context_window": 8192
            },
            "bug_detection": {
                "model": "gpt-4o-mini",
                "temperature": 0.3,
                "max_tokens": 2000,
                "context_window": 8192
            },
            "commit_message": {
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                "max_tokens": 500,
                "context_window": 4096
            },
            "code_refactoring": {
                "model": "gpt-4o-mini",
                "temperature": 0.5,
                "max_tokens": 3000,
                "context_window": 8192
            },
            "documentation": {
                "model": "gpt-4o-mini",
                "temperature": 0.7,
                "max_tokens": 2000,
                "context_window": 8192
            }
        }
        
        self.contexts = {}
        self.model_usage = {}

    def get_model_config(self, task_type: str) -> Dict[str, Any]:
        """
        Get the configuration for a specific task type.
        
        Args:
            task_type: Type of task (e.g., "code_analysis", "bug_detection")
            
        Returns:
            Dictionary containing model configuration
        """
        try:
            if task_type not in self.models:
                st.warning(f"Task type {task_type} not found. Using default configuration.")
                return self.models["code_analysis"]
            return self.models[task_type]
        except Exception as e:
            logger.error(f"Error getting model config: {str(e)}")
            st.error(f"Error getting model configuration: {str(e)}")
            return self.models["code_analysis"]

    def update_model_config(self, task_type: str, config: Dict[str, Any]) -> bool:
        """
        Update the configuration for a specific task type.
        
        Args:
            task_type: The type of task to update
            config: New configuration dictionary
            
        Returns:
            Boolean indicating success
        """
        try:
            if task_type in self.models:
                self.models[task_type].update(config)
                return True
            return False
        except Exception as e:
            logger.error(f"Error updating model config: {str(e)}")
            return False

    def get_context(self, task_type: str) -> Optional[Dict[str, Any]]:
        """
        Get the context for a specific task type.
        
        Args:
            task_type: The type of task to get context for
            
        Returns:
            Dictionary containing context information
        """
        return self.contexts.get(task_type)

    def update_context(self, task_type: str, context: Dict[str, Any]) -> bool:
        """
        Update the context for a specific task type.
        
        Args:
            task_type: The type of task to update context for
            context: New context dictionary
            
        Returns:
            Boolean indicating success
        """
        try:
            self.contexts[task_type] = context
            return True
        except Exception as e:
            logger.error(f"Error updating context: {str(e)}")
            return False

    def track_usage(self, task_type: str, tokens_used: int) -> None:
        """
        Track model usage statistics.
        
        Args:
            task_type: Type of task
            tokens_used: Number of tokens used
        """
        try:
            if task_type not in self.model_usage:
                self.model_usage[task_type] = {
                    "total_tokens": 0,
                    "requests": 0
                }
            
            self.model_usage[task_type]["total_tokens"] += tokens_used
            self.model_usage[task_type]["requests"] += 1
            
            # Show usage in Streamlit
            st.sidebar.markdown(f"### Model Usage for {task_type}")
            st.sidebar.markdown(f"Total Tokens: {self.model_usage[task_type]['total_tokens']}")
            st.sidebar.markdown(f"Requests: {self.model_usage[task_type]['requests']}")
            
        except Exception as e:
            logger.error(f"Error tracking model usage: {str(e)}")
            st.error(f"Error tracking model usage: {str(e)}")

    def get_usage_stats(self) -> Dict[str, Any]:
        """
        Get usage statistics for all models.
        
        Returns:
            Dictionary containing usage statistics
        """
        return self.model_usage

    def optimize_model_selection(self, task_type: str, input_size: int) -> Dict[str, Any]:
        """
        Optimize model selection based on input size and task type.
        
        Args:
            task_type: The type of task
            input_size: Size of the input in tokens
            
        Returns:
            Dictionary containing optimized model configuration
        """
        config = self.get_model_config(task_type)
        
        # Adjust model based on input size
        if input_size > 4000 and task_type != "code_analysis":
            config["model"] = "gpt-4"
            config["max_tokens"] = 4000
        elif input_size <= 4000 and task_type in ["code_analysis", "bug_detection"]:
            config["model"] = "gpt-3.5-turbo"
            config["max_tokens"] = 2000
            
        return config

    def get_model_prompt(self, task_type: str) -> str:
        """
        Get the appropriate prompt template for a task type.
        
        Args:
            task_type: The type of task
            
        Returns:
            String containing the prompt template
        """
        prompts = {
            "code_analysis": """Analyze the following code for:
            1. Code quality and best practices
            2. Potential bugs and issues
            3. Performance optimizations
            4. Security vulnerabilities
            5. Documentation needs
            
            Code:
            {code}
            
            Provide a detailed analysis with specific recommendations.""",
            
            "bug_detection": """Detect potential bugs in the following code:
            1. Runtime errors
            2. Logic errors
            3. Security vulnerabilities
            4. Performance issues
            5. Edge cases
            
            Code:
            {code}
            
            List all potential issues with explanations and suggested fixes.""",
            
            "commit_message": """Generate a clear and descriptive commit message for the following changes:
            
            Changes:
            {changes}
            
            Follow conventional commit format and include relevant details.""",
            
            "code_refactoring": """Suggest refactoring improvements for the following code:
            1. Code organization
            2. Design patterns
            3. Performance optimizations
            4. Readability improvements
            5. Maintainability enhancements
            
            Code:
            {code}
            
            Provide specific refactoring suggestions with code examples."""
        }
        
        return prompts.get(task_type, prompts["code_analysis"]) 