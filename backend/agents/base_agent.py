"""
Base Agent Class
All specialized agents inherit from this to ensure consistent interface
"""
from abc import ABC, abstractmethod
from anthropic import Anthropic
from typing import Any, Dict, List
from pydantic import BaseModel

from config import get_settings

settings = get_settings()


class AgentResponse(BaseModel):
    """Standard response format for all agents"""
    agent_name: str
    success: bool
    data: Dict[str, Any]
    reasoning: str
    confidence: float = 1.0  # 0.0 to 1.0


class BaseAgent(ABC):
    """
    Abstract base class for all specialized agents
    Provides common functionality like API access and logging
    """
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        self.model = "claude-3-sonnet-20240229"  # Worker agents use Sonnet for speed
        self.max_tokens = 2000
        
    @abstractmethod
    def process(self, context: Dict[str, Any]) -> AgentResponse:
        """
        Each agent must implement this method
        
        Args:
            context: Dictionary containing all information the agent needs
        
        Returns:
            AgentResponse with structured output
        """
        pass
    
    def _call_claude(self, system_prompt: str, user_message: str, temperature: float = 0.7) -> str:
        """
        Shared method for calling Claude API
        All agents use this to maintain consistency
        """
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"{self.agent_name} API call failed: {str(e)}")
            raise
    
    def log_activity(self, message: str):
        """Log agent activity for debugging"""
        print(f"[{self.agent_name}] {message}")