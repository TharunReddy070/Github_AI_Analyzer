import os
import tempfile
import shutil
from typing import List, Dict, Any
import logging
from github import Github
from app.core.config import settings
import streamlit as st

logger = logging.getLogger(__name__)

class GitHubAnalyzer:
    def __init__(self):
        """Initialize GitHub analyzer with authentication."""
        self.github = Github(settings.GITHUB_TOKEN)
        self.temp_dir = tempfile.mkdtemp()

    async def analyze_repository(self, repo_url: str) -> Dict[str, Any]:
        """
        Analyze a GitHub repository.
        
        Args:
            repo_url: GitHub repository URL
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            with st.spinner(f"Analyzing repository: {repo_url}"):
                # Extract repository details
                repo_name = repo_url.split("/")[-1]
                owner = repo_url.split("/")[-2]
                
                # Get repository
                repo = self.github.get_repo(f"{owner}/{repo_name}")
                
                # Clone repository
                clone_path = os.path.join(self.temp_dir, repo_name)
                if os.path.exists(clone_path):
                    shutil.rmtree(clone_path)
                repo.clone(clone_path)
                
                # Analyze repository
                results = {
                    "repository": {
                        "name": repo.name,
                        "owner": repo.owner.login,
                        "description": repo.description,
                        "stars": repo.stargazers_count,
                        "forks": repo.forks_count,
                        "issues": repo.open_issues_count,
                        "language": repo.language,
                        "created_at": repo.created_at.isoformat(),
                        "updated_at": repo.updated_at.isoformat()
                    },
                    "code_analysis": await self._analyze_codebase(clone_path),
                    "security_analysis": await self._analyze_security(repo),
                    "dependency_analysis": await self._analyze_dependencies(repo),
                    "test_coverage": await self._analyze_test_coverage(repo),
                    "documentation": await self._analyze_documentation(repo)
                }
                
                # Cleanup
                shutil.rmtree(clone_path)
                
                return results
                
        except Exception as e:
            logger.error(f"Error analyzing repository: {str(e)}")
            st.error(f"Error analyzing repository: {str(e)}")
            return {
                "error": str(e),
                "repository_url": repo_url
            }

    async def _analyze_codebase(self, repo_path: str) -> Dict[str, Any]:
        """Analyze the codebase for quality and issues."""
        results = {
            "total_files": 0,
            "total_lines": 0,
            "languages": {},
            "complexity": {},
            "issues": []
        }
        
        for root, _, files in os.walk(repo_path):
            for file in files:
                if file.endswith(('.py', '.js', '.java', '.cpp', '.c', '.h', '.cs', '.go', '.rs')):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        results["total_files"] += 1
                        results["total_lines"] += len(content.splitlines())
                        
                        # Language-specific analysis
                        lang = file.split('.')[-1]
                        if lang not in results["languages"]:
                            results["languages"][lang] = 0
                        results["languages"][lang] += 1
                        
                        # Add to issues if any found
                        issues = self._check_code_issues(content, lang)
                        if issues:
                            results["issues"].extend(issues)
        
        return results

    async def _analyze_security(self, repo) -> Dict[str, Any]:
        """Analyze repository for security issues."""
        results = {
            "vulnerabilities": [],
            "security_headers": {},
            "dependencies": {}
        }
        
        # Check for security advisories
        try:
            advisories = repo.get_vulnerability_alert()
            if advisories:
                results["vulnerabilities"].extend(advisories)
        except:
            pass
        
        # Check for security policy
        try:
            security_policy = repo.get_contents("SECURITY.md")
            results["security_policy"] = True
        except:
            results["security_policy"] = False
        
        return results

    async def _analyze_dependencies(self, repo) -> Dict[str, Any]:
        """Analyze repository dependencies."""
        results = {
            "dependencies": {},
            "outdated_packages": [],
            "vulnerable_packages": []
        }
        
        # Check for dependency files
        dependency_files = [
            "requirements.txt",
            "package.json",
            "pom.xml",
            "build.gradle",
            "Cargo.toml",
            "go.mod"
        ]
        
        for file in dependency_files:
            try:
                content = repo.get_contents(file)
                results["dependencies"][file] = self._parse_dependencies(content.decoded_content.decode())
            except:
                continue
        
        return results

    async def _analyze_test_coverage(self, repo) -> Dict[str, Any]:
        """Analyze test coverage and quality."""
        results = {
            "test_files": [],
            "coverage_reports": [],
            "test_framework": None
        }
        
        # Check for test files
        test_patterns = [
            "test_",
            "_test",
            "spec_",
            "_spec",
            "tests/",
            "specs/"
        ]
        
        for pattern in test_patterns:
            try:
                test_files = repo.get_contents("", ref="main")
                for file in test_files:
                    if pattern in file.name:
                        results["test_files"].append(file.name)
            except:
                continue
        
        return results

    async def _analyze_documentation(self, repo) -> Dict[str, Any]:
        """Analyze repository documentation."""
        results = {
            "has_readme": False,
            "has_contributing": False,
            "has_license": False,
            "documentation_files": []
        }
        
        # Check for documentation files
        doc_files = [
            "README.md",
            "CONTRIBUTING.md",
            "LICENSE",
            "docs/"
        ]
        
        for file in doc_files:
            try:
                repo.get_contents(file)
                if file == "README.md":
                    results["has_readme"] = True
                elif file == "CONTRIBUTING.md":
                    results["has_contributing"] = True
                elif file == "LICENSE":
                    results["has_license"] = True
                else:
                    results["documentation_files"].append(file)
            except:
                continue
        
        return results

    def _check_code_issues(self, content: str, language: str) -> List[Dict[str, Any]]:
        """Check code for common issues."""
        issues = []
        
        # Security issues
        if language == "python":
            if "eval(" in content:
                issues.append({
                    "type": "security",
                    "severity": "high",
                    "message": "Use of eval() detected",
                    "language": language
                })
        
        # Performance issues
        if "while True:" in content and "break" not in content:
            issues.append({
                "type": "performance",
                "severity": "medium",
                "message": "Potential infinite loop detected",
                "language": language
            })
        
        return issues

    def _parse_dependencies(self, content: str) -> Dict[str, str]:
        """Parse dependency file content."""
        dependencies = {}
        
        for line in content.splitlines():
            if line and not line.startswith('#'):
                try:
                    if '==' in line:
                        package, version = line.split('==')
                        dependencies[package.strip()] = version.strip()
                except:
                    continue
        
        return dependencies 