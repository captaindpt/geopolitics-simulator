from typing import Optional
from .base_action import Action
from .specific_actions import DeclareWarAction, ProposeAllianceAction, HelpAction

class ActionFactory:
    @staticmethod
    def create_action(decision: str, source: str) -> Optional[Action]:
        """
        Create appropriate action from decision text
        
        Args:
            decision: The decision text from an agent
            source: The name of the country making the decision
            
        Returns:
            Action if decision can be parsed, None otherwise
        """
        # Extract target country from decision
        words = decision.split()
        
        if decision.startswith("Declare war on "):
            target = words[-1]  # Last word is target country
            return DeclareWarAction(decision, source, target)
            
        if decision.startswith("Propose alliance to "):
            target = words[-1]  # Last word is target country
            return ProposeAllianceAction(decision, source, target)
            
        if decision.startswith("Help "):
            # Format: "Help X against their enemies" or "Help X"
            target = words[1]  # Second word is target country
            return HelpAction(decision, source, target)
            
        if decision == "Mobilize forces":
            return None  # Not implemented yet
            
        if decision.startswith("Sue for peace with "):
            target = words[-1]  # Last word is target country
            return None  # Not implemented yet
            
        return None 