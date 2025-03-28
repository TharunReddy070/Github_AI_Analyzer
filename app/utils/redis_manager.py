import redis
import json
import os
import logging
import streamlit as st
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RedisManager:
    def __init__(self):
        # Initialize in-memory fallback storage
        self.memory_cache = {
            "analysis_results": {},
            "code_analysis": {},
            "web_tests": {},
            "user_preferences": {}
        }
        
        # Try to connect to Redis
        try:
            self.redis = redis.Redis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                db=int(os.getenv("REDIS_DB", 0)),
                password=os.getenv("REDIS_PASSWORD", None),
                socket_timeout=5,
                decode_responses=True
            )
            # Test connection
            self.redis.ping()
            self.redis_available = True
            logger.info("Connected to Redis successfully")
            st.success("Redis connected successfully!")
        except (redis.ConnectionError, redis.exceptions.TimeoutError) as e:
            self.redis_available = False
            logger.warning(f"Redis connection failed: {e}. Using in-memory fallback.")
            st.warning(f"Redis connection failed: {e}. Using in-memory fallback.")
    
    def _store_in_redis(self, key, value, expires=None):
        """Store data in Redis with optional expiration"""
        if self.redis_available:
            try:
                self.redis.set(key, json.dumps(value))
                if expires:
                    self.redis.expire(key, expires)
                return True
            except Exception as e:
                logger.error(f"Error storing in Redis: {e}")
                return False
        return False
    
    def _get_from_redis(self, key):
        """Get data from Redis"""
        if self.redis_available:
            try:
                data = self.redis.get(key)
                if data:
                    return json.loads(data)
            except Exception as e:
                logger.error(f"Error retrieving from Redis: {e}")
        return None
    
    # GitHub Analysis Results
    def store_analysis_result(self, repo_url, results):
        """Store GitHub repository analysis results"""
        key = f"github_analysis:{repo_url}"
        success = self._store_in_redis(key, results)
        if not success:
            self.memory_cache["analysis_results"][repo_url] = results
        return True
    
    def get_analysis_result(self, repo_url):
        """Get GitHub repository analysis results"""
        key = f"github_analysis:{repo_url}"
        result = self._get_from_redis(key)
        if result is None and repo_url in self.memory_cache["analysis_results"]:
            return self.memory_cache["analysis_results"][repo_url]
        return result
    
    # Code Analysis Results
    def store_code_analysis(self, code_id, results):
        """Store code analysis results"""
        key = f"code_analysis:{code_id}"
        success = self._store_in_redis(key, results)
        if not success:
            self.memory_cache["code_analysis"][code_id] = results
        return True
    
    def get_code_analysis(self, code_id):
        """Get code analysis results"""
        key = f"code_analysis:{code_id}"
        result = self._get_from_redis(key)
        if result is None and code_id in self.memory_cache["code_analysis"]:
            return self.memory_cache["code_analysis"][code_id]
        return result
    
    # Web Test Results
    def store_web_test_result(self, url, results):
        """Store web test results"""
        key = f"web_test:{url}"
        success = self._store_in_redis(key, results)
        if not success:
            self.memory_cache["web_tests"][url] = results
        return True
    
    def get_web_test_result(self, url):
        """Get web test results"""
        key = f"web_test:{url}"
        result = self._get_from_redis(key)
        if result is None and url in self.memory_cache["web_tests"]:
            return self.memory_cache["web_tests"][url]
        return result
    
    # User Preferences
    def store_user_preferences(self, user_id, preferences):
        """Store user preferences"""
        key = f"user_prefs:{user_id}"
        success = self._store_in_redis(key, preferences)
        if not success:
            self.memory_cache["user_preferences"][user_id] = preferences
        return True
    
    def get_user_preferences(self, user_id):
        """Get user preferences"""
        key = f"user_prefs:{user_id}"
        result = self._get_from_redis(key)
        if result is None and user_id in self.memory_cache["user_preferences"]:
            return self.memory_cache["user_preferences"][user_id]
        return result

    def store_agent_message(self, agent_id: str, message: dict) -> bool:
        """Store agent message."""
        try:
            key = f"agent:{agent_id}:messages"
            message['timestamp'] = datetime.now().isoformat()
            self.redis.rpush(key, json.dumps(message))
            return True
        except Exception as e:
            logger.error(f"Failed to store agent message: {str(e)}")
            return False

    def get_agent_messages(self, agent_id: str) -> list:
        """Retrieve agent messages."""
        try:
            key = f"agent:{agent_id}:messages"
            messages = self.redis.lrange(key, 0, -1)
            return [json.loads(msg) for msg in messages]
        except Exception as e:
            logger.error(f"Failed to get agent messages: {str(e)}")
            return []

    def clear_agent_messages(self, agent_id: str) -> bool:
        """Clear agent messages."""
        try:
            key = f"agent:{agent_id}:messages"
            self.redis.delete(key)
            return True
        except Exception as e:
            logger.error(f"Failed to clear agent messages: {str(e)}")
            return False

    def store_task_status(self, task_id: str, status: dict) -> bool:
        """Store task status."""
        try:
            key = f"task:{task_id}:status"
            status['timestamp'] = datetime.now().isoformat()
            self.redis.setex(
                key,
                7200,  # 2 hours expiry
                json.dumps(status)
            )
            return True
        except Exception as e:
            logger.error(f"Failed to store task status: {str(e)}")
            return False

    def get_task_status(self, task_id: str) -> dict:
        """Retrieve task status."""
        try:
            key = f"task:{task_id}:status"
            status = self.redis.get(key)
            return json.loads(status) if status else None
        except Exception as e:
            logger.error(f"Failed to get task status: {str(e)}")
            return None

    def close(self):
        """Close Redis connection."""
        try:
            self.redis.close()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Failed to close Redis connection: {str(e)}") 