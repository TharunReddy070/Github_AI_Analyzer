import streamlit as st
from app.agents.code_review_agent import CodeReviewAgent
from app.utils.web_automation import WebAutomation
from app.utils.github_analyzer import GitHubAnalyzer
from app.core.model_manager import ModelManager
import os
from dotenv import load_dotenv
from app.utils.redis_manager import RedisManager
import json
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize agents and managers
code_review_agent = CodeReviewAgent()
web_automation = WebAutomation()
github_analyzer = GitHubAnalyzer()
model_manager = ModelManager()
redis_manager = RedisManager()

# Set page config
st.set_page_config(
    page_title="GitHub AI Analyzer",
    page_icon="🤖",
    layout="wide"
)

# Sidebar
st.sidebar.title("Settings")
st.sidebar.markdown("### Configuration")

# API Keys
openai_key = st.sidebar.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
github_token = st.sidebar.text_input("GitHub Token", type="password", value=os.getenv("GITHUB_TOKEN", ""))
github_username = st.sidebar.text_input("GitHub Username", value=os.getenv("GITHUB_USERNAME", ""))

# Main content
st.markdown("""
    <h1 style='text-align: center; color: #FF4B4B;'>
        🤖 GitHub AI Analyzer
    </h1>
    <h3 style='text-align: center; color: #666666;'>
        Intelligent Code Analysis & Repository Management
    </h3>
""", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; color: #666666; margin-bottom: 20px;'>
        Analyze repositories, detect issues, and improve code quality with AI-powered insights
    </div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["GitHub Analysis", "Code Review", "Web Automation", "Model Management"])

# GitHub Analysis Tab
with tab1:
    st.header("GitHub Repository Analysis")
    repo_url = st.text_input("Enter GitHub Repository URL:", placeholder="https://github.com/username/repo")
    if st.button("Analyze Repository"):
        if repo_url:
            with st.spinner("Analyzing repository..."):
                # Check if analysis exists in Redis
                cached_analysis = redis_manager.get_analysis_result(repo_url)
                
                if cached_analysis:
                    st.info("Using cached repository analysis")
                    st.json(cached_analysis)
                else:
                    # Perform new analysis
                    analysis_results = github_analyzer.analyze_repository(repo_url)
                    
                    # Store in Redis
                    redis_manager.store_analysis_result(repo_url, analysis_results)
                    
                    # Display repository information
                    st.subheader("Repository Information")
                    repo_info = analysis_results.get("repository", {})
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Stars", repo_info.get("stars", 0))
                        st.metric("Forks", repo_info.get("forks", 0))
                    with col2:
                        st.metric("Open Issues", repo_info.get("issues", 0))
                        st.metric("Language", repo_info.get("language", "Unknown"))
                    with col3:
                        st.metric("Created", repo_info.get("created_at", "Unknown"))
                        st.metric("Last Updated", repo_info.get("updated_at", "Unknown"))
                    
                    # Display code analysis
                    st.subheader("Code Analysis")
                    code_analysis = analysis_results.get("code_analysis", {})
                    st.metric("Total Files", code_analysis.get("total_files", 0))
                    st.metric("Total Lines", code_analysis.get("total_lines", 0))
                    
                    # Display issues
                    if code_analysis.get("issues"):
                        st.subheader("Issues Found")
                        for issue in code_analysis["issues"]:
                            st.warning(f"{issue['type'].title()} Issue: {issue['message']}")
                    
                    # Display security analysis
                    st.subheader("Security Analysis")
                    security = analysis_results.get("security_analysis", {})
                    if security.get("vulnerabilities"):
                        st.error("Security Vulnerabilities Found!")
                        for vuln in security["vulnerabilities"]:
                            st.error(f"Vulnerability: {vuln}")
                    
                    # Display dependency analysis
                    st.subheader("Dependency Analysis")
                    deps = analysis_results.get("dependency_analysis", {})
                    if deps.get("dependencies"):
                        st.write("Dependencies:")
                        for file, packages in deps["dependencies"].items():
                            st.write(f"**{file}:**")
                            for pkg, version in packages.items():
                                st.write(f"- {pkg}: {version}")
                    
                    # Display test coverage
                    st.subheader("Test Coverage")
                    tests = analysis_results.get("test_coverage", {})
                    if tests.get("test_files"):
                        st.write("Test Files Found:")
                        for file in tests["test_files"]:
                            st.write(f"- {file}")
                    
                    # Display documentation
                    st.subheader("Documentation")
                    docs = analysis_results.get("documentation", {})
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("README", "✅" if docs.get("has_readme") else "❌")
                    with col2:
                        st.metric("Contributing", "✅" if docs.get("has_contributing") else "❌")
                    with col3:
                        st.metric("License", "✅" if docs.get("has_license") else "❌")
        else:
            st.warning("Please enter a GitHub repository URL.")

# Code Review Tab
with tab2:
    st.header("Code Review")
    code_input = st.text_area("Enter code to analyze:", height=200)
    if st.button("Analyze Code"):
        if code_input:
            with st.spinner("Analyzing code..."):
                # Check if analysis exists in Redis
                code_id = hash(code_input)
                cached_analysis = redis_manager.get_code_analysis(code_id)
                
                if cached_analysis:
                    st.info("Using cached analysis")
                    st.json(cached_analysis)
                else:
                    # Perform new analysis
                    analysis_results = code_review_agent.analyze_code(code_input)
                    
                    # Store in Redis
                    redis_manager.store_code_analysis(code_id, analysis_results)
                    
                    # Display results
                    st.json(analysis_results)
        else:
            st.warning("Please enter some code to analyze.")

# Web Automation Tab
with tab3:
    st.header("Web Automation")
    url = st.text_input("Enter URL to test:")
    if st.button("Run Tests"):
        if url:
            with st.spinner("Running web automation tests..."):
                # Check if test results exist in Redis
                cached_results = redis_manager.get_web_test_result(url)
                
                if cached_results:
                    st.info("Using cached test results")
                    st.json(cached_results)
                else:
                    # Run new tests
                    test_results = web_automation.run_automated_tests(url)
                    
                    # Store in Redis
                    redis_manager.store_web_test_result(url, test_results)
                    
                    # Display results
                    st.json(test_results)
        else:
            st.warning("Please enter a URL to test.")

# Model Management Tab
with tab4:
    st.header("Model Management")
    task_type = st.selectbox(
        "Select Task Type",
        ["code_analysis", "bug_detection", "code_refactoring"]
    )
    if st.button("Get Model Config"):
        config = model_manager.get_model_config(task_type)
        st.json(config)
    
    # Usage Statistics
    st.subheader("Model Usage Statistics")
    usage_stats = model_manager.get_usage_stats()
    st.json(usage_stats)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666666;'>
        Made with ❤️ using Streamlit & OpenAI
    </div>
""", unsafe_allow_html=True)

# Add sidebar for user preferences
with st.sidebar:
    st.header("User Preferences")
    
    # Get user preferences from Redis
    user_id = "default_user"  # In a real app, this would be from authentication
    user_prefs = redis_manager.get_user_preferences(user_id) or {}
    
    # Preference options
    theme = st.selectbox(
        "Theme",
        ["Light", "Dark"],
        index=0 if user_prefs.get("theme") == "Light" else 1
    )
    
    analysis_depth = st.slider(
        "Analysis Depth",
        1, 5,
        value=user_prefs.get("analysis_depth", 3)
    )
    
    # Save preferences
    if st.button("Save Preferences"):
        preferences = {
            "theme": theme,
            "analysis_depth": analysis_depth,
            "last_updated": datetime.now().isoformat()
        }
        redis_manager.store_user_preferences(user_id, preferences)
        st.success("Preferences saved!")

if __name__ == "__main__":
    main() 