from typing import List, Dict, Any, Optional
import json
import os
from app.core.config import settings
from app.core.model_manager import ModelManager
import logging
import re
from datetime import datetime
import streamlit as st

logger = logging.getLogger(__name__)

class CodeReviewAgent:
    def __init__(self):
        """Initialize the CodeReviewAgent with advanced capabilities."""
        self.model_manager = ModelManager()
    
    async def analyze_code(self, 
                          code: str, 
                          language: str,
                          context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Perform comprehensive code analysis.
        
        Args:
            code: The code to analyze
            language: Programming language
            context: Additional context information
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            with st.spinner("Analyzing code..."):
                # Get model configuration
                model_config = self.model_manager.get_model_config("code_analysis")
                
                # Prepare the prompt
                prompt = self._prepare_analysis_prompt(code, language, context)
                
                # Get analysis from model
                analysis_result = await self._get_model_analysis(prompt, model_config)
                
                # Extract and structure the results
                results = {
                    "timestamp": datetime.now().isoformat(),
                    "language": language,
                    "metrics": self._extract_metrics(code, language),
                    "complexity": self._calculate_complexity(code, language),
                    "dependencies": self._extract_dependencies(code, language),
                    "test_coverage": self._estimate_test_coverage(code, language),
                    "security_issues": self._check_security(code, language),
                    "performance_issues": self._check_performance(code, language),
                    "maintainability": self._check_maintainability(code, language),
                    "quality_issues": self._extract_quality_issues(analysis_result),
                    "security_vulnerabilities": self._extract_security_vulnerabilities(analysis_result),
                    "performance_optimizations": self._extract_performance_issues(analysis_result),
                    "best_practices": self._extract_best_practices(analysis_result),
                    "improvement_suggestions": self._extract_improvement_suggestions(analysis_result),
                    "structure_analysis": self._extract_structure_analysis(analysis_result)
                }
                
                # Track model usage
                self.model_manager.track_usage("code_analysis", len(prompt.split()))
                
                return results
                
        except Exception as e:
            logger.error(f"Error in code analysis: {str(e)}")
            st.error(f"Error analyzing code: {str(e)}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }

    def _prepare_analysis_prompt(self, code: str, language: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Prepare the analysis prompt."""
        prompt = self.model_manager.get_model_prompt("code_analysis")
        return prompt.format(
            code=code,
            language=language,
            context=json.dumps(context) if context else "{}"
        )

    async def _get_model_analysis(self, prompt: str, model_config: Dict[str, Any]) -> Dict[str, Any]:
        """Get analysis from the model."""
        try:
            # Use the model manager to get the response
            response = await self.model_manager.get_completion(prompt, model_config)
            return json.loads(response)
        except Exception as e:
            logger.error(f"Error getting model analysis: {str(e)}")
            return {}

    def _extract_metrics(self, code: str, language: str) -> Dict[str, Any]:
        """Extract code metrics."""
        metrics = {
            "lines_of_code": len(code.splitlines()),
            "complexity": self._calculate_complexity(code, language),
            "dependencies": self._extract_dependencies(code, language),
            "test_coverage": self._estimate_test_coverage(code, language)
        }
        return metrics

    def _calculate_complexity(self, code: str, language: str) -> Dict[str, Any]:
        """Calculate code complexity metrics."""
        complexity = {
            "cyclomatic": 0,
            "cognitive": 0,
            "maintainability": 0
        }
        
        # Basic cyclomatic complexity calculation
        control_structures = [
            r"if\s*\([^)]*\)",
            r"for\s*\([^)]*\)",
            r"while\s*\([^)]*\)",
            r"switch\s*\([^)]*\)",
            r"catch\s*\([^)]*\)"
        ]
        
        for structure in control_structures:
            complexity["cyclomatic"] += len(re.findall(structure, code))
        
        # Add 1 for the main function
        complexity["cyclomatic"] += 1
        
        return complexity

    def _extract_dependencies(self, code: str, language: str) -> List[str]:
        """Extract code dependencies."""
        dependencies = []
        
        if language.lower() == "python":
            # Extract import statements
            imports = re.findall(r"^(?:from|import)\s+(\w+)", code, re.MULTILINE)
            dependencies.extend(imports)
        elif language.lower() == "javascript":
            # Extract require/import statements
            requires = re.findall(r"require\(['\"]([^'\"]+)['\"]\)", code)
            imports = re.findall(r"import\s+(?:from\s+)?['\"]([^'\"]+)['\"]", code)
            dependencies.extend(requires + imports)
            
        return list(set(dependencies))

    def _estimate_test_coverage(self, code: str, language: str) -> Dict[str, Any]:
        """Estimate test coverage based on code analysis."""
        coverage = {
            "unit_tests": 0,
            "integration_tests": 0,
            "total_coverage": 0
        }
        
        # Look for test files and test functions
        test_patterns = {
            "python": [
                r"def\s+test_",
                r"class\s+Test",
                r"pytest",
                r"unittest"
            ],
            "javascript": [
                r"test\(",
                r"describe\(",
                r"it\(",
                r"jest"
            ]
        }
        
        patterns = test_patterns.get(language.lower(), [])
        for pattern in patterns:
            matches = re.findall(pattern, code, re.IGNORECASE)
            coverage["unit_tests"] += len(matches)
        
        # Estimate total coverage based on test presence
        if coverage["unit_tests"] > 0:
            coverage["total_coverage"] = min(100, coverage["unit_tests"] * 10)
        
        return coverage

    def _check_security(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Check for security vulnerabilities."""
        security_issues = []
        
        # Common security patterns to check
        security_patterns = {
            "python": [
                (r"eval\(", "Use of eval() is dangerous"),
                (r"exec\(", "Use of exec() is dangerous"),
                (r"os\.system\(", "Use of os.system() is dangerous"),
                (r"subprocess\.call\(", "Use of subprocess.call() is dangerous"),
                (r"pickle\.loads\(", "Use of pickle.loads() is dangerous")
            ],
            "javascript": [
                (r"eval\(", "Use of eval() is dangerous"),
                (r"new\s+Function\(", "Use of Function constructor is dangerous"),
                (r"innerHTML\s*=", "Use of innerHTML is dangerous"),
                (r"document\.write\(", "Use of document.write() is dangerous")
            ]
        }
        
        patterns = security_patterns.get(language.lower(), [])
        for pattern, message in patterns:
            matches = re.findall(pattern, code)
            if matches:
                security_issues.append({
                    "type": "security",
                    "severity": "high",
                    "message": message,
                    "line_numbers": self._find_line_numbers(code, pattern)
                })
        
        return security_issues

    def _check_performance(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Check for performance issues."""
        performance_issues = []
        
        # Common performance patterns to check
        performance_patterns = {
            "python": [
                (r"for\s+.*\s+in\s+range\(len\(", "Use enumerate() instead of range(len())"),
                (r"\+\s*=\s*['\"]\w+['\"]", "Use list comprehension or join() for string concatenation"),
                (r"\.append\(.*\)\s*for\s+.*\s+in", "Use list comprehension instead of loop with append()")
            ],
            "javascript": [
                (r"for\s*\(\s*var\s+i", "Use let instead of var in for loops"),
                (r"\.forEach\(\s*function\s*\(", "Use arrow function in forEach"),
                (r"document\.getElementsBy", "Use querySelector for better performance")
            ]
        }
        
        patterns = performance_patterns.get(language.lower(), [])
        for pattern, message in patterns:
            matches = re.findall(pattern, code)
            if matches:
                performance_issues.append({
                    "type": "performance",
                    "severity": "medium",
                    "message": message,
                    "line_numbers": self._find_line_numbers(code, pattern)
                })
        
        return performance_issues

    def _check_maintainability(self, code: str, language: str) -> List[Dict[str, Any]]:
        """Check for maintainability issues."""
        maintainability_issues = []
        
        # Common maintainability patterns to check
        maintainability_patterns = {
            "python": [
                (r"def\s+\w+\s*\([^)]{120,}\)", "Function signature is too long"),
                (r"if.*(?:and|or).*(?:and|or)", "Complex conditional statement"),
                (r"global\s+\w+", "Use of global variables")
            ],
            "javascript": [
                (r"function\s*\([^)]{120,}\)", "Function signature is too long"),
                (r"if.*&&.*&&", "Complex conditional statement"),
                (r"var\s+\w+\s*=\s*function", "Use const/let and arrow functions")
            ]
        }
        
        patterns = maintainability_patterns.get(language.lower(), [])
        for pattern, message in patterns:
            matches = re.findall(pattern, code)
            if matches:
                maintainability_issues.append({
                    "type": "maintainability",
                    "severity": "medium",
                    "message": message,
                    "line_numbers": self._find_line_numbers(code, pattern)
                })
        
        return maintainability_issues

    def _find_line_numbers(self, code: str, pattern: str) -> List[int]:
        """Find line numbers for a pattern in code."""
        lines = code.splitlines()
        line_numbers = []
        for i, line in enumerate(lines, 1):
            if re.search(pattern, line):
                line_numbers.append(i)
        return line_numbers

    def _extract_quality_issues(self, analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract code quality issues from analysis result."""
        return analysis_result.get("quality_issues", [])

    def _extract_security_vulnerabilities(self, analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract security vulnerabilities from analysis result."""
        return analysis_result.get("security_vulnerabilities", [])

    def _extract_performance_issues(self, analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract performance issues from analysis result."""
        return analysis_result.get("performance_issues", [])

    def _extract_best_practices(self, analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract best practices from analysis result."""
        return analysis_result.get("best_practices", [])

    def _extract_improvement_suggestions(self, analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract improvement suggestions from analysis result."""
        return analysis_result.get("improvement_suggestions", [])

    def _extract_structure_analysis(self, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Extract code structure analysis from analysis result."""
        return analysis_result.get("structure_analysis", {}) 