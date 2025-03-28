from redis import Redis
from app.core.config import settings
import json
import logging
from datetime import datetime
import streamlit as st

logger = logging.getLogger(__name__)

class RedisManager:
    def __init__(self):
        """Initialize Redis connection."""
        try:
            self.redis = Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                decode_responses=True
            )
            self.redis.ping()  # Test connection
            logger.info("Redis connection established successfully")
            st.success("Redis connected successfully!")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {str(e)}")
            st.error(f"Redis connection failed: {str(e)}")
            raise

    def store_analysis_result(self, repo_url: str, result: dict) -> bool:
        """Store repository analysis result."""
        try:
            key = f"analysis:{repo_url}"
            result['timestamp'] = datetime.now().isoformat()
            self.redis.setex(
                key,
                3600,  # 1 hour expiry
                json.dumps(result)
            )
            return True
        except Exception as e:
            logger.error(f"Failed to store analysis result: {str(e)}")
            return False

    def get_analysis_result(self, repo_url: str) -> dict:
        """Retrieve repository analysis result."""
        try:
            key = f"analysis:{repo_url}"
            result = self.redis.get(key)
            return json.loads(result) if result else None
        except Exception as e:
            logger.error(f"Failed to get analysis result: {str(e)}")
            return None

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

    def store_code_analysis(self, code_id: str, analysis: dict) -> bool:
        """Store code analysis results."""
        try:
            key = f"code_analysis:{code_id}"
            analysis['timestamp'] = datetime.now().isoformat()
            self.redis.setex(
                key,
                3600,  # 1 hour expiry
                json.dumps(analysis)
            )
            return True
        except Exception as e:
            logger.error(f"Failed to store code analysis: {str(e)}")
            return False

    def get_code_analysis(self, code_id: str) -> dict:
        """Retrieve code analysis results."""
        try:
            key = f"code_analysis:{code_id}"
            analysis = self.redis.get(key)
            return json.loads(analysis) if analysis else None
        except Exception as e:
            logger.error(f"Failed to get code analysis: {str(e)}")
            return None

    def store_web_test_result(self, url: str, result: dict) -> bool:
        """Store web test results."""
        try:
            key = f"web_test:{url}"
            result['timestamp'] = datetime.now().isoformat()
            self.redis.setex(
                key,
                3600,  # 1 hour expiry
                json.dumps(result)
            )
            return True
        except Exception as e:
            logger.error(f"Failed to store web test result: {str(e)}")
            return False

    def get_web_test_result(self, url: str) -> dict:
        """Retrieve web test results."""
        try:
            key = f"web_test:{url}"
            result = self.redis.get(key)
            return json.loads(result) if result else None
        except Exception as e:
            logger.error(f"Failed to get web test result: {str(e)}")
            return None

    def store_user_preferences(self, user_id: str, preferences: dict) -> bool:
        """Store user preferences."""
        try:
            key = f"user_prefs:{user_id}"
            self.redis.setex(
                key,
                86400,  # 24 hours expiry
                json.dumps(preferences)
            )
            return True
        except Exception as e:
            logger.error(f"Failed to store user preferences: {str(e)}")
            return False

    def get_user_preferences(self, user_id: str) -> dict:
        """Retrieve user preferences."""
        try:
            key = f"user_prefs:{user_id}"
            prefs = self.redis.get(key)
            return json.loads(prefs) if prefs else None
        except Exception as e:
            logger.error(f"Failed to get user preferences: {str(e)}")
            return None

    def close(self):
        """Close Redis connection."""
        try:
            self.redis.close()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Failed to close Redis connection: {str(e)}") 