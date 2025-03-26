from actions.base_action import BaseAction
from models.world import World

class IssueUltimatumAction(BaseAction):
    """Action for issuing an ultimatum to another country."""
    
    def execute(self, world: World) -> bool:
        """Execute the ultimatum."""
        if not self.target:
            return False
            
        # Add the event
        world.add_event(f"{self.source} issues ultimatum to {self.target}")
        return True
        
    def get_description(self) -> str:
        return f"{self.source} issues ultimatum to {self.target}" 