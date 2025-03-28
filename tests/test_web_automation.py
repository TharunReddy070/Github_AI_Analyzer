import pytest
from app.utils.web_automation import WebAutomation
from playwright.async_api import async_playwright
import json

@pytest.fixture
async def web_automation():
    automation = WebAutomation()
    yield automation
    await automation.close()

@pytest.mark.asyncio
async def test_run_automated_tests(web_automation):
    """Test running automated tests on a website."""
    url = "https://example.com"
    
    results = await web_automation.run_automated_tests(url)
    
    assert isinstance(results, dict)
    assert "timestamp" in results
    assert "url" in results
    assert "accessibility" in results
    assert "performance" in results
    assert "security" in results

@pytest.mark.asyncio
async def test_run_automated_tests_with_scenarios(web_automation):
    """Test running automated tests with custom scenarios."""
    url = "https://example.com"
    test_scenarios = {
        "click_button": {
            "selector": "button",
            "action": "click",
            "expected": "success"
        },
        "check_text": {
            "selector": "h1",
            "action": "text",
            "expected": "Example Domain"
        }
    }
    
    results = await web_automation.run_automated_tests(url, test_scenarios)
    
    assert isinstance(results, dict)
    assert "test_scenarios" in results
    assert isinstance(results["test_scenarios"], dict)
    assert len(results["test_scenarios"]) == len(test_scenarios)

@pytest.mark.asyncio
async def test_accessibility_check(web_automation):
    """Test accessibility checking."""
    url = "https://example.com"
    
    results = await web_automation.run_automated_tests(url)
    
    assert "accessibility" in results
    accessibility = results["accessibility"]
    assert "title" in accessibility
    assert "headings" in accessibility
    assert "links" in accessibility
    assert "images" in accessibility

@pytest.mark.asyncio
async def test_performance_check(web_automation):
    """Test performance checking."""
    url = "https://example.com"
    
    results = await web_automation.run_automated_tests(url)
    
    assert "performance" in results
    performance = results["performance"]
    assert "load_time" in performance
    assert "resource_count" in performance
    assert "resource_size" in performance

@pytest.mark.asyncio
async def test_security_check(web_automation):
    """Test security checking."""
    url = "https://example.com"
    
    results = await web_automation.run_automated_tests(url)
    
    assert "security" in results
    security = results["security"]
    assert "headers" in security
    assert "certificates" in security
    assert "vulnerabilities" in security

@pytest.mark.asyncio
async def test_error_handling(web_automation):
    """Test error handling for invalid URLs."""
    url = "https://invalid-url-that-does-not-exist.com"
    
    results = await web_automation.run_automated_tests(url)
    
    assert isinstance(results, dict)
    assert "error" in results
    assert "timestamp" in results

@pytest.mark.asyncio
async def test_custom_browser_options(web_automation):
    """Test using custom browser options."""
    url = "https://example.com"
    browser_options = {
        "headless": True,
        "slow_mo": 50,
        "viewport": {
            "width": 1920,
            "height": 1080
        }
    }
    
    results = await web_automation.run_automated_tests(url, browser_options=browser_options)
    
    assert isinstance(results, dict)
    assert "error" not in results

@pytest.mark.asyncio
async def test_screenshot_capture(web_automation):
    """Test capturing screenshots during tests."""
    url = "https://example.com"
    
    results = await web_automation.run_automated_tests(url, capture_screenshot=True)
    
    assert isinstance(results, dict)
    assert "screenshots" in results
    assert isinstance(results["screenshots"], list)
    assert len(results["screenshots"]) > 0 