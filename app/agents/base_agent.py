from crewai import Agent
from langchain.memory import ConversationBufferMemory
from app.core.config import settings
from typing import Dict, Any, Optional

class BaseAgent:
    def __init__(
        self,
        role: str,
        goal: str,
        backstory: str,
        verbose: bool = True,
        allow_delegation: bool = False,
        memory: bool = True
    ):
        """Initialize the base agent with CrewAI configuration."""
        # Initialize memory if enabled
        agent_memory = None
        if memory:
            agent_memory = ConversationBufferMemory(
                memory_key="chat_history",
                return_messages=True
            )

        # Create the CrewAI agent
        self.agent = Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            verbose=verbose,
            allow_delegation=allow_delegation,
            memory=agent_memory,
            llm_config={
                "model": settings.CREWAI_MODEL,
                "temperature": float(settings.CREWAI_TEMPERATURE),
                "max_tokens": int(settings.CREWAI_MAX_TOKENS)
            }
        )

    async def execute_task(self, task: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a task with the agent."""
        try:
            # Add context to task if provided
            if context:
                task = f"{task}\nContext: {context}"

            # Execute the task
            result = await self.agent.execute(task)

            return {
                "status": "success",
                "result": result
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_memory(self) -> Optional[ConversationBufferMemory]:
        """Get the agent's memory"""
        return self.agent.memory
    
    def clear_memory(self):
        """Clear the agent's memory"""
        if self.agent.memory:
            self.agent.memory.clear() 