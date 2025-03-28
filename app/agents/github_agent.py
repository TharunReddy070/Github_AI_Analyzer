from typing import List, Dict, Any, Optional
import logging
from github import Github, Repository, Issue, PullRequest
from app.core.config import settings
import streamlit as st
from datetime import datetime, timedelta
import re

logger = logging.getLogger(__name__)

class GitHubAgent:
    def __init__(self):
        """Initialize GitHub agent with authentication."""
        self.github = Github(settings.GITHUB_TOKEN)
        self.username = settings.GITHUB_USERNAME

    async def analyze_user_repositories(self) -> Dict[str, Any]:
        """Analyze all repositories of the authenticated user."""
        try:
            with st.spinner("Analyzing your repositories..."):
                user = self.github.get_user()
                repos = user.get_repos()
                
                results = {
                    "user": {
                        "username": user.login,
                        "name": user.name,
                        "bio": user.bio,
                        "public_repos": user.public_repos,
                        "followers": user.followers,
                        "following": user.following
                    },
                    "repositories": []
                }
                
                for repo in repos:
                    repo_data = await self.analyze_repository(repo.full_name)
                    results["repositories"].append(repo_data)
                
                return results
        except Exception as e:
            logger.error(f"Error analyzing user repositories: {str(e)}")
            st.error(f"Error analyzing repositories: {str(e)}")
            return {"error": str(e)}

    async def create_issue(self, repo_name: str, title: str, body: str, labels: List[str] = None) -> Dict[str, Any]:
        """Create a new issue in a repository."""
        try:
            with st.spinner("Creating issue..."):
                repo = self.github.get_repo(repo_name)
                issue = repo.create_issue(
                    title=title,
                    body=body,
                    labels=labels or []
                )
                return {
                    "number": issue.number,
                    "title": issue.title,
                    "url": issue.html_url,
                    "state": issue.state
                }
        except Exception as e:
            logger.error(f"Error creating issue: {str(e)}")
            st.error(f"Error creating issue: {str(e)}")
            return {"error": str(e)}

    async def create_pull_request(self, 
                                repo_name: str, 
                                title: str, 
                                body: str, 
                                head: str, 
                                base: str = "main") -> Dict[str, Any]:
        """Create a new pull request."""
        try:
            with st.spinner("Creating pull request..."):
                repo = self.github.get_repo(repo_name)
                pr = repo.create_pull(
                    title=title,
                    body=body,
                    head=head,
                    base=base
                )
                return {
                    "number": pr.number,
                    "title": pr.title,
                    "url": pr.html_url,
                    "state": pr.state
                }
        except Exception as e:
            logger.error(f"Error creating pull request: {str(e)}")
            st.error(f"Error creating pull request: {str(e)}")
            return {"error": str(e)}

    async def analyze_issues(self, repo_name: str) -> Dict[str, Any]:
        """Analyze issues in a repository."""
        try:
            with st.spinner("Analyzing issues..."):
                repo = self.github.get_repo(repo_name)
                issues = repo.get_issues(state="all")
                
                results = {
                    "total_issues": 0,
                    "open_issues": 0,
                    "closed_issues": 0,
                    "issues_by_label": {},
                    "issues_by_assignee": {},
                    "recent_issues": [],
                    "stale_issues": []
                }
                
                for issue in issues:
                    results["total_issues"] += 1
                    if issue.state == "open":
                        results["open_issues"] += 1
                    else:
                        results["closed_issues"] += 1
                    
                    # Group by labels
                    for label in issue.labels:
                        if label.name not in results["issues_by_label"]:
                            results["issues_by_label"][label.name] = 0
                        results["issues_by_label"][label.name] += 1
                    
                    # Group by assignee
                    if issue.assignee:
                        assignee = issue.assignee.login
                        if assignee not in results["issues_by_assignee"]:
                            results["issues_by_assignee"][assignee] = 0
                        results["issues_by_assignee"][assignee] += 1
                    
                    # Recent issues
                    if issue.created_at > datetime.now() - timedelta(days=7):
                        results["recent_issues"].append({
                            "number": issue.number,
                            "title": issue.title,
                            "state": issue.state,
                            "created_at": issue.created_at.isoformat()
                        })
                    
                    # Stale issues (no activity for 30 days)
                    if issue.state == "open" and issue.updated_at < datetime.now() - timedelta(days=30):
                        results["stale_issues"].append({
                            "number": issue.number,
                            "title": issue.title,
                            "last_updated": issue.updated_at.isoformat()
                        })
                
                return results
        except Exception as e:
            logger.error(f"Error analyzing issues: {str(e)}")
            st.error(f"Error analyzing issues: {str(e)}")
            return {"error": str(e)}

    async def analyze_pull_requests(self, repo_name: str) -> Dict[str, Any]:
        """Analyze pull requests in a repository."""
        try:
            with st.spinner("Analyzing pull requests..."):
                repo = self.github.get_repo(repo_name)
                prs = repo.get_pulls(state="all")
                
                results = {
                    "total_prs": 0,
                    "open_prs": 0,
                    "merged_prs": 0,
                    "closed_prs": 0,
                    "prs_by_author": {},
                    "recent_prs": [],
                    "stale_prs": []
                }
                
                for pr in prs:
                    results["total_prs"] += 1
                    if pr.state == "open":
                        results["open_prs"] += 1
                    elif pr.merged:
                        results["merged_prs"] += 1
                    else:
                        results["closed_prs"] += 1
                    
                    # Group by author
                    author = pr.user.login
                    if author not in results["prs_by_author"]:
                        results["prs_by_author"][author] = 0
                    results["prs_by_author"][author] += 1
                    
                    # Recent PRs
                    if pr.created_at > datetime.now() - timedelta(days=7):
                        results["recent_prs"].append({
                            "number": pr.number,
                            "title": pr.title,
                            "state": pr.state,
                            "created_at": pr.created_at.isoformat()
                        })
                    
                    # Stale PRs (no activity for 7 days)
                    if pr.state == "open" and pr.updated_at < datetime.now() - timedelta(days=7):
                        results["stale_prs"].append({
                            "number": pr.number,
                            "title": pr.title,
                            "last_updated": pr.updated_at.isoformat()
                        })
                
                return results
        except Exception as e:
            logger.error(f"Error analyzing pull requests: {str(e)}")
            st.error(f"Error analyzing pull requests: {str(e)}")
            return {"error": str(e)}

    async def suggest_improvements(self, repo_name: str) -> Dict[str, Any]:
        """Suggest improvements for a repository."""
        try:
            with st.spinner("Generating improvement suggestions..."):
                repo = self.github.get_repo(repo_name)
                
                suggestions = {
                    "documentation": [],
                    "testing": [],
                    "security": [],
                    "performance": [],
                    "maintenance": []
                }
                
                # Check documentation
                try:
                    repo.get_contents("README.md")
                except:
                    suggestions["documentation"].append("Add a README.md file")
                
                try:
                    repo.get_contents("CONTRIBUTING.md")
                except:
                    suggestions["documentation"].append("Add CONTRIBUTING.md guidelines")
                
                # Check testing
                test_files = [f for f in repo.get_contents("") if "test" in f.name.lower()]
                if not test_files:
                    suggestions["testing"].append("Add test files")
                
                # Check security
                try:
                    repo.get_contents("SECURITY.md")
                except:
                    suggestions["security"].append("Add SECURITY.md policy")
                
                # Check dependencies
                try:
                    repo.get_contents("requirements.txt")
                except:
                    suggestions["maintenance"].append("Add requirements.txt")
                
                # Check for stale issues
                issues = await self.analyze_issues(repo_name)
                if issues.get("stale_issues"):
                    suggestions["maintenance"].append("Address stale issues")
                
                # Check for stale PRs
                prs = await self.analyze_pull_requests(repo_name)
                if prs.get("stale_prs"):
                    suggestions["maintenance"].append("Address stale pull requests")
                
                return suggestions
        except Exception as e:
            logger.error(f"Error generating suggestions: {str(e)}")
            st.error(f"Error generating suggestions: {str(e)}")
            return {"error": str(e)}

    async def generate_release_notes(self, repo_name: str, tag: str) -> Dict[str, Any]:
        """Generate release notes for a repository."""
        try:
            with st.spinner("Generating release notes..."):
                repo = self.github.get_repo(repo_name)
                
                # Get commits since last release
                try:
                    last_release = repo.get_latest_release()
                    since = last_release.created_at
                except:
                    since = repo.created_at
                
                commits = repo.get_commits(since=since)
                
                # Categorize changes
                changes = {
                    "features": [],
                    "fixes": [],
                    "improvements": [],
                    "other": []
                }
                
                for commit in commits:
                    message = commit.commit.message.lower()
                    if "feat" in message or "feature" in message:
                        changes["features"].append(commit.commit.message)
                    elif "fix" in message or "bug" in message:
                        changes["fixes"].append(commit.commit.message)
                    elif "improve" in message or "enhance" in message:
                        changes["improvements"].append(commit.commit.message)
                    else:
                        changes["other"].append(commit.commit.message)
                
                return {
                    "tag": tag,
                    "changes": changes,
                    "total_commits": commits.totalCount
                }
        except Exception as e:
            logger.error(f"Error generating release notes: {str(e)}")
            st.error(f"Error generating release notes: {str(e)}")
            return {"error": str(e)} 