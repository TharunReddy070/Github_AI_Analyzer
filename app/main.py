from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.agents.code_review_agent import CodeReviewAgent
from app.utils.web_automation import WebAutomation
from app.core.model_manager import ModelManager
from typing import Dict, Any, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
code_review_agent = CodeReviewAgent()
web_automation = WebAutomation()
model_manager = ModelManager()

@app.get("/")
async def root():
    """Root endpoint returning basic information about the service."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "operational"
    }

@app.post("/api/v1/analyze-code")
async def analyze_code(
    code: str,
    language: str,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Analyze code using the CodeReviewAgent.
    
    Args:
        code: The code to analyze
        language: Programming language
        context: Additional context information
        
    Returns:
        Analysis results including metrics, security issues, and suggestions
    """
    try:
        result = await code_review_agent.analyze_code(code, language, context)
        return result
    except Exception as e:
        logger.error(f"Error analyzing code: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analyze-web")
async def analyze_web(
    url: str,
    test_scenarios: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Analyze a website using WebAutomation.
    
    Args:
        url: The website URL to analyze
        test_scenarios: Custom test scenarios to run
        
    Returns:
        Analysis results including accessibility, performance, and security metrics
    """
    try:
        results = web_automation.run_automated_tests(url, test_scenarios)
        return results
    except Exception as e:
        logger.error(f"Error analyzing website: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/model-stats")
async def get_model_stats() -> Dict[str, Any]:
    """
    Get model usage statistics.
    
    Returns:
        Statistics about model usage including token counts and request counts
    """
    try:
        stats = model_manager.get_usage_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting model stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/model-config/{task_type}")
async def get_model_config(task_type: str) -> Dict[str, Any]:
    """
    Get model configuration for a specific task type.
    
    Args:
        task_type: Type of task (e.g., code_analysis, bug_detection)
        
    Returns:
        Model configuration for the specified task type
    """
    try:
        config = model_manager.get_model_config(task_type)
        return config
    except KeyError:
        raise HTTPException(status_code=404, detail=f"Task type {task_type} not found")
    except Exception as e:
        logger.error(f"Error getting model config: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 