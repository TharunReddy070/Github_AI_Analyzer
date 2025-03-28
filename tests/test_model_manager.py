import pytest
from app.core.model_manager import ModelManager
from app.core.config import settings

@pytest.fixture
def model_manager():
    """Create a ModelManager instance for testing."""
    return ModelManager()

def test_get_model_config(model_manager):
    """Test getting model configuration."""
    config = model_manager.get_model_config("code_analysis")
    
    assert isinstance(config, dict)
    assert "model" in config
    assert "temperature" in config
    assert "max_tokens" in config
    assert "context_window" in config
    assert config["model"] == "gpt-4o-mini"

def test_get_model_config_default(model_manager):
    """Test getting default model configuration for unknown task."""
    config = model_manager.get_model_config("unknown_task")
    
    assert isinstance(config, dict)
    assert config == model_manager.models["code_analysis"]

def test_update_model_config(model_manager):
    """Test updating model configuration."""
    new_config = {
        "model": "gpt-4o-mini",
        "temperature": 0.8,
        "max_tokens": 3000
    }
    
    success = model_manager.update_model_config("code_analysis", new_config)
    assert success
    
    updated_config = model_manager.get_model_config("code_analysis")
    assert updated_config["temperature"] == 0.8
    assert updated_config["max_tokens"] == 3000

def test_update_model_config_invalid(model_manager):
    """Test updating model configuration for invalid task."""
    new_config = {
        "model": "gpt-4o-mini",
        "temperature": 0.8
    }
    
    success = model_manager.update_model_config("invalid_task", new_config)
    assert not success

def test_get_context(model_manager):
    """Test getting context."""
    context = model_manager.get_context("code_analysis")
    assert context is None

def test_update_context(model_manager):
    """Test updating context."""
    new_context = {
        "repository": "test-repo",
        "branch": "main",
        "file": "test.py"
    }
    
    success = model_manager.update_context("code_analysis", new_context)
    assert success
    
    context = model_manager.get_context("code_analysis")
    assert context == new_context

def test_track_usage(model_manager):
    """Test tracking model usage."""
    model_manager.track_usage("code_analysis", 100)
    
    stats = model_manager.get_usage_stats()
    assert "code_analysis" in stats
    assert stats["code_analysis"]["total_tokens"] == 100
    assert stats["code_analysis"]["requests"] == 1
    
    model_manager.track_usage("code_analysis", 50)
    stats = model_manager.get_usage_stats()
    assert stats["code_analysis"]["total_tokens"] == 150
    assert stats["code_analysis"]["requests"] == 2

def test_optimize_model_selection(model_manager):
    """Test model selection optimization."""
    config = model_manager.optimize_model_selection("code_analysis", 5000)
    
    assert isinstance(config, dict)
    assert "model" in config
    assert "max_tokens" in config
    
    config = model_manager.optimize_model_selection("bug_detection", 3000)
    assert config["model"] == "gpt-3.5-turbo"
    assert config["max_tokens"] == 2000

def test_get_model_prompt(model_manager):
    """Test getting model prompts."""
    prompt = model_manager.get_model_prompt("code_analysis")
    
    assert isinstance(prompt, str)
    assert "Code:" in prompt
    assert "Analyze" in prompt
    
    prompt = model_manager.get_model_prompt("bug_detection")
    assert isinstance(prompt, str)
    assert "Code:" in prompt
    assert "Detect" in prompt
    
    # Test default prompt for unknown task type
    prompt = model_manager.get_model_prompt("unknown_task")
    assert isinstance(prompt, str)
    assert prompt == model_manager.get_model_prompt("code_analysis")

def test_get_usage_stats(model_manager):
    """Test getting usage statistics."""
    task_types = ["code_analysis", "bug_detection", "code_refactoring"]
    
    for task_type in task_types:
        model_manager.track_usage(task_type, 100)
    
    stats = model_manager.get_usage_stats()
    
    assert len(stats) == len(task_types)
    for task_type in task_types:
        assert task_type in stats
        assert stats[task_type]["total_tokens"] == 100
        assert stats[task_type]["request_count"] == 1

def test_reset_usage_stats(model_manager):
    """Test resetting usage statistics."""
    task_type = "code_analysis"
    model_manager.track_usage(task_type, 100)
    
    model_manager.reset_usage_stats()
    stats = model_manager.get_usage_stats()
    
    assert stats[task_type]["total_tokens"] == 0
    assert stats[task_type]["request_count"] == 0 