from playwright.sync_api import sync_playwright
from typing import Optional, Dict, Any
import logging
from app.core.config import settings
import streamlit as st
from datetime import datetime

logger = logging.getLogger(__name__)

class WebAutomation:
    def __init__(self):
        """Initialize Playwright and browser context."""
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def run_automated_tests(self, url: str, test_scenarios: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Run automated tests on the specified URL.
        
        Args:
            url: The URL to test
            test_scenarios: Dictionary of test scenarios to run
            
        Returns:
            Dict containing test results
        """
        try:
            with st.spinner("Running web automation tests..."):
                results = {
                    "url": url,
                    "tests": [],
                    "status": "success",
                    "timestamp": datetime.now().isoformat()
                }
                
                # Navigate to URL
                self.page.goto(url)
                
                # Basic accessibility test
                accessibility = self.page.evaluate("""() => {
                    return {
                        title: document.title,
                        headings: Array.from(document.getElementsByTagName('h1')).map(h => h.textContent),
                        links: Array.from(document.getElementsByTagName('a')).map(a => a.href),
                        images: Array.from(document.getElementsByTagName('img')).map(img => img.alt)
                    }
                }""")
                
                results["tests"].append({
                    "name": "accessibility_check",
                    "status": "success",
                    "data": accessibility
                })
                
                # Performance metrics
                performance = self.page.evaluate("""() => {
                    const timing = window.performance.timing;
                    return {
                        loadTime: timing.loadEventEnd - timing.navigationStart,
                        domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
                        firstPaint: performance.getEntriesByType('paint')[0]?.startTime,
                        resources: performance.getEntriesByType('resource').map(r => ({
                            name: r.name,
                            duration: r.duration,
                            size: r.transferSize
                        }))
                    }
                }""")
                
                results["tests"].append({
                    "name": "performance_metrics",
                    "status": "success",
                    "data": performance
                })
                
                # Security headers
                security = self.check_security_headers(url)
                results["tests"].append({
                    "name": "security_headers",
                    "status": "success",
                    "data": security
                })
                
                # Custom test scenarios
                if test_scenarios:
                    for name, scenario in test_scenarios.items():
                        try:
                            result = self._run_test_scenario(scenario)
                            results["tests"].append({
                                "name": name,
                                "status": "success",
                                "data": result
                            })
                        except Exception as e:
                            logger.error(f"Error in test scenario {name}: {str(e)}")
                            results["tests"].append({
                                "name": name,
                                "status": "error",
                                "error": str(e)
                            })
                
                return results
                
        except Exception as e:
            logger.error(f"Error in web automation: {str(e)}")
            st.error(f"Error running web automation tests: {str(e)}")
            return {
                "url": url,
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
        finally:
            self.cleanup()

    def check_security_headers(self, url: str) -> Dict[str, Any]:
        """
        Check security headers of the website.
        
        Args:
            url: The URL to check
            
        Returns:
            Dict containing security header information
        """
        try:
            self.page.goto(url)
            headers = self.page.evaluate("""() => {
                return {
                    'Content-Security-Policy': document.querySelector('meta[http-equiv="Content-Security-Policy"]')?.content,
                    'X-Frame-Options': document.querySelector('meta[http-equiv="X-Frame-Options"]')?.content,
                    'X-Content-Type-Options': document.querySelector('meta[http-equiv="X-Content-Type-Options"]')?.content,
                    'Strict-Transport-Security': document.querySelector('meta[http-equiv="Strict-Transport-Security"]')?.content
                }
            }""")
            
            return {
                "url": url,
                "status": "success",
                "headers": headers
            }
            
        except Exception as e:
            logger.error(f"Error checking security headers: {str(e)}")
            return {
                "url": url,
                "status": "error",
                "error": str(e)
            }
        finally:
            self.cleanup()

    def cleanup(self):
        """Clean up resources."""
        try:
            self.context.close()
            self.browser.close()
            self.playwright.stop()
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}") 