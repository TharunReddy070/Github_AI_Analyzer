# AI-Powered GitHub Auto-Manager

A comprehensive AI-powered tool for automated code review, analysis, and web testing with GitHub integration. This project leverages advanced AI models to provide intelligent insights and automation for software development workflows.

## 🌟 Features

### 1. Code Analysis
- **Intelligent Code Review**: Automated analysis of code quality, best practices, and potential issues
- **Security Scanning**: Detection of security vulnerabilities and compliance issues
- **Performance Optimization**: Identification of performance bottlenecks and optimization opportunities
- **Maintainability Assessment**: Evaluation of code maintainability and complexity
- **Documentation Analysis**: Review of documentation completeness and quality

### 2. Web Testing Automation
- **Accessibility Testing**: Comprehensive accessibility compliance checks
- **Performance Metrics**: Detailed performance analysis and optimization suggestions
- **Security Headers**: Verification of security headers and best practices
- **Custom Test Scenarios**: Support for custom test cases and scenarios
- **Screenshot Capture**: Automated screenshot capture for visual regression testing

### 3. GitHub Integration
- **Repository Analysis**: Deep analysis of GitHub repositories
- **Issue Management**: Automated issue tracking and management
- **Pull Request Review**: Intelligent PR review and suggestions
- **Release Notes Generation**: Automated generation of release notes
- **Repository Health Monitoring**: Continuous monitoring of repository health

## 🚀 Getting Started

### Prerequisites
- Python 3.11.8 or higher
- Git
- GitHub account with appropriate permissions
- OpenAI API key

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/yourusername/ai-github-manager.git
cd ai-github-manager
```

2. **Set Up Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# For Windows:
venv\Scripts\activate
# For Unix/MacOS:
source venv/bin/activate
```

3. **Install Dependencies**
```bash
# Install packages
pip install -r packages.txt

# Install Playwright browsers
playwright install
```

4. **Configure Environment Variables**
Create a `.env` file in the project root:
```env
# GitHub Configuration
GITHUB_TOKEN=your_github_token
GITHUB_USERNAME=your_github_username

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
```

## 💻 Usage

### 1. Starting the Application
```bash
streamlit run app/streamlit_app.py
```

### 2. Code Analysis
1. Navigate to the "Code Analysis" tab
2. Enter your code in the text area
3. Select analysis options:
   - Code Quality
   - Security
   - Performance
   - Maintainability
4. Click "Analyze Code"
5. View detailed analysis results and recommendations

### 3. Web Testing
1. Navigate to the "Web Testing" tab
2. Enter the URL to test
3. Select test options:
   - Accessibility
   - Performance
   - Security
   - Custom Scenarios
4. Click "Run Tests"
5. Review test results and metrics

### 4. GitHub Analysis
1. Navigate to the "GitHub Analysis" tab
2. Enter a GitHub repository URL
3. Select analysis options:
   - Repository Health
   - Code Quality
   - Security
   - Dependencies
4. Click "Analyze Repository"
5. View comprehensive repository analysis

## 📊 Output Schema

### Repository Analysis Results
```json
{
    "repository": {
        "name": "repository-name",
        "owner": "owner-name",
        "description": "repository description",
        "stars": 123,
        "forks": 45,
        "open_issues": 10,
        "language": "Python",
        "created_at": "2024-03-26T12:00:00Z",
        "updated_at": "2024-03-26T12:00:00Z"
    },
    "code_analysis": {
        "total_files": 150,
        "total_lines": 5000,
        "languages": {
            "Python": {
                "files": 100,
                "lines": 3000
            }
        },
        "issues": [
            {
                "type": "security",
                "severity": "high",
                "message": "Use of eval() is dangerous",
                "file": "src/main.py",
                "line": 42
            }
        ]
    },
    "security": {
        "vulnerabilities": [],
        "policies": {
            "has_security_policy": true,
            "has_code_of_conduct": true
        }
    },
    "dependencies": {
        "requirements.txt": [
            {
                "package": "requests",
                "version": "2.25.0",
                "latest_version": "2.31.0"
            }
        ]
    },
    "test_coverage": {
        "test_files": 25,
        "frameworks": ["pytest"],
        "coverage_percentage": 85
    },
    "documentation": {
        "has_readme": true,
        "has_contributing": true,
        "has_license": true
    },
    "performance": {
        "build_time": "2m 30s",
        "test_time": "1m 15s",
        "dependencies_count": 45
    },
    "maintainability": {
        "score": 85,
        "factors": {
            "code_complexity": "medium",
            "documentation_quality": "high"
        }
    },
    "summary": {
        "health_score": 88,
        "risk_level": "low",
        "recommendations": [
            "Update outdated dependencies",
            "Add more test coverage"
        ]
    }
}
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=app tests/
```

### Test Categories
- Unit Tests
- Integration Tests
- End-to-End Tests
- Performance Tests

## 🔧 Configuration

### Model Configuration
The project uses different AI models for various tasks:
- Code Analysis: GPT-4o-mini
- Bug Detection: GPT-4o-mini
- Documentation: GPT-4o-mini
- Issue Analysis: GPT-4o-mini
- PR Review: GPT-4o-mini

### Customization Options
- Model parameters (temperature, max_tokens)
- Analysis thresholds
- Test scenarios
- Output formats

## 📝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

For support, please:
1. Check the documentation
2. Search existing issues
3. Create a new issue if needed

## 🔄 Updates and Maintenance

### Regular Updates
- Dependencies are updated monthly
- Security patches are applied immediately
- New features are added quarterly

### Version History
- v1.0.0: Initial release
- v1.1.0: Added GitHub integration
- v1.2.0: Enhanced web testing capabilities

## 📚 Additional Resources

- [Documentation](docs/)
- [API Reference](docs/api.md)
- [Contributing Guidelines](CONTRIBUTING.md)
- [Security Policy](SECURITY.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)

## 🙏 Acknowledgments

- OpenAI for providing the AI models
- GitHub for the API and integration
- The open-source community for various tools and libraries 