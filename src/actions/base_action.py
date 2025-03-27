from __future__ import annotations
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.world import World

class Action:
    def __init__(self, text: str, source: str, target: Optional[str] = None):
        """
        Initialize an action
        
        Args:
            text: Human-readable description of the action
            source: Name of the country initiating the action
            target: Optional name of the target country
        """
        self.text = text
        self.source = source
        self.target = target
        
    def execute(self, world: 'World') -> bool:
        """
        Execute the action in the given world
        
        Args:
            world: The world state to modify
            
        Returns:
            bool: True if action was successful, False otherwise
        """
        raise NotImplementedError("Subclasses must implement execute") 