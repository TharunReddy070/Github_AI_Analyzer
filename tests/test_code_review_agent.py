import pytest
from app.agents.code_review_agent import CodeReviewAgent
from app.core.model_manager import ModelManager
import json

@pytest.fixture
def code_review_agent():
    """Create a CodeReviewAgent instance for testing."""
    return CodeReviewAgent()

@pytest.fixture
def sample_python_code():
    return """
def calculate_sum(numbers):
    total = 0
    for i in range(len(numbers)):
        total += numbers[i]
    return total

def process_data(data):
    result = eval(data)
    return result * 2
"""

@pytest.fixture
def sample_javascript_code():
    return """
function calculateSum(numbers) {
    var total = 0;
    for (var i = 0; i < numbers.length; i++) {
        total += numbers[i];
    }
    return total;
}

function processData(data) {
    var result = eval(data);
    document.write(result);
    return result * 2;
}
"""

@pytest.mark.asyncio
async def test_analyze_code_python(code_review_agent, sample_python_code):
    result = await code_review_agent.analyze_code(sample_python_code, "python")
    
    assert isinstance(result, dict)
    assert "timestamp" in result
    assert "language" in result
    assert result["language"] == "python"
    
    # Check metrics
    assert "metrics" in result
    assert isinstance(result["metrics"], dict)
    assert "lines_of_code" in result["metrics"]
    
    # Check security issues
    assert "security_issues" in result
    security_issues = result["security_issues"]
    assert isinstance(security_issues, list)
    assert any(issue["message"] == "Use of eval() is dangerous" for issue in security_issues)
    
    # Check performance issues
    assert "performance_issues" in result
    performance_issues = result["performance_issues"]
    assert isinstance(performance_issues, list)
    assert any(issue["message"] == "Use enumerate() instead of range(len())" for issue in performance_issues)

@pytest.mark.asyncio
async def test_analyze_code_javascript(code_review_agent, sample_javascript_code):
    result = await code_review_agent.analyze_code(sample_javascript_code, "javascript")
    
    assert isinstance(result, dict)
    assert "timestamp" in result
    assert "language" in result
    assert result["language"] == "javascript"
    
    # Check security issues
    assert "security_issues" in result
    security_issues = result["security_issues"]
    assert isinstance(security_issues, list)
    assert any(issue["message"] == "Use of eval() is dangerous" for issue in security_issues)
    assert any(issue["message"] == "Use of document.write() is dangerous" for issue in security_issues)
    
    # Check performance issues
    assert "performance_issues" in result
    performance_issues = result["performance_issues"]
    assert isinstance(performance_issues, list)
    assert any(issue["message"] == "Use let instead of var in for loops" for issue in performance_issues)

def test_extract_dependencies_python(code_review_agent):
    code = """
import os
from datetime import datetime
import json as js
from typing import List, Dict
"""
    deps = code_review_agent._extract_dependencies(code, "python")
    assert isinstance(deps, list)
    assert "os" in deps
    assert "datetime" in deps
    assert "json" in deps
    assert "typing" in deps

def test_extract_dependencies_javascript(code_review_agent):
    code = """
const fs = require('fs');
import { useState } from 'react';
import axios from 'axios';
"""
    deps = code_review_agent._extract_dependencies(code, "javascript")
    assert isinstance(deps, list)
    assert "fs" in deps
    assert "react" in deps
    assert "axios" in deps

def test_calculate_complexity(code_review_agent):
    code = """
def complex_function(x):
    if x > 0:
        for i in range(10):
            while i < 5:
                if i == 3:
                    break
    return x
"""
    complexity = code_review_agent._calculate_complexity(code, "python")
    assert isinstance(complexity, dict)
    assert "cyclomatic" in complexity
    assert complexity["cyclomatic"] > 1  # Should count multiple control structures

def test_estimate_test_coverage(code_review_agent):
    code = """
def test_function():
    assert True

class TestClass:
    def test_method(self):
        assert 1 == 1

def not_a_test():
    pass
"""
    coverage = code_review_agent._estimate_test_coverage(code, "python")
    assert isinstance(coverage, dict)
    assert "unit_tests" in coverage
    assert coverage["unit_tests"] > 0
    assert "total_coverage" in coverage

@pytest.mark.asyncio
async def test_error_handling(code_review_agent):
    result = await code_review_agent.analyze_code("", "unknown_language")
    assert isinstance(result, dict)
    assert "error" in result
    assert "timestamp" in result

def test_extract_metrics(code_review_agent):
    """Test metrics extraction."""
    code = """
import os
import sys

def main():
    print("Hello, World!")
    """
    language = "python"
    
    metrics = code_review_agent._extract_metrics(code, language)
    
    assert "lines_of_code" in metrics
    assert "complexity" in metrics
    assert "dependencies" in metrics
    assert "test_coverage" in metrics
    assert metrics["dependencies"] == ["os", "sys"]

def test_check_security(code_review_agent):
    """Test security vulnerability checks."""
    code = """
import os
import subprocess

def dangerous_function():
    os.system("rm -rf /")
    subprocess.call(["echo", "dangerous"])
    eval("print('hello')")
    """
    language = "python"
    
    security_issues = code_review_agent._check_security(code, language)
    
    assert len(security_issues) > 0
    for issue in security_issues:
        assert "type" in issue
        assert "description" in issue
        assert "line" in issue
        assert "code" in issue

def test_check_performance(code_review_agent):
    """Test performance issue checks."""
    code = """
def slow_function():
    result = []
    for i in range(1000):
        result.append(i)
    return result
    """
    language = "python"
    
    performance_issues = code_review_agent._check_performance(code, language)
    
    assert len(performance_issues) > 0
    for issue in performance_issues:
        assert "type" in issue
        assert "description" in issue
        assert "line" in issue
        assert "code" in issue

def test_check_maintainability(code_review_agent):
    """Test maintainability checks."""
    code = """
def long_function():
    # This is a very long function with many lines
    # that should trigger maintainability warnings
    for i in range(100):
        if i % 2 == 0:
            print("Even number")
        else:
            print("Odd number")
    return True
    """
    language = "python"
    
    maintainability = code_review_agent._check_maintainability(code, language)
    
    assert "score" in maintainability
    assert "issues" in maintainability
    assert maintainability["score"] < 100
    assert len(maintainability["issues"]) > 0

def test_extract_function_body(code_review_agent):
    """Test function body extraction."""
    code = """
def test_function():
    print("Line 1")
    print("Line 2")
    return True

def another_function():
    print("Different function")
    """
    
    body = code_review_agent._extract_function_body(code, code.find("def test_function()") + len("def test_function():"))
    
    assert "print(\"Line 1\")" in body
    assert "print(\"Line 2\")" in body
    assert "return True" in body
    assert "print(\"Different function\")" not in body

@pytest.mark.asyncio
async def test_analyze_codebase(code_review_agent):
    """Test codebase analysis."""
    repo_path = "tests/test_repo"
    result = await code_review_agent.analyze_codebase(repo_path)
    
    assert isinstance(result, dict)
    assert "status" in result
    assert "files_analyzed" in result
    assert "total_issues" in result
    assert "summary" in result

def test_language_specific_checks(code_review_agent):
    """Test language-specific code checks."""
    python_code = """
def python_function():
    print("Hello")
    """
    js_code = """
function jsFunction() {
    console.log("Hello");
}
    """
    
    python_issues = code_review_agent._check_security(python_code, "python")
    js_issues = code_review_agent._check_security(js_code, "javascript")
    
    assert isinstance(python_issues, list)
    assert isinstance(js_issues, list)
    assert len(python_issues) != len(js_issues)  # Different patterns for different languages 