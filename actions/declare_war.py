from actions.base_action import BaseAction
from models.world import World

class DeclareWarAction(BaseAction):
    """Action for declaring war on another country."""
    
    def execute(self, world: World) -> bool:
        """Execute the war declaration."""
        if not self.target:
            return False
            
        # Add the conflict
        conflict = f"{self.source}-{self.target}"
        world.add_conflict(conflict)
        
        # Add the event
        world.add_event(f"{self.source} declares war on {self.target}")
        return True
        
    def get_description(self) -> str:
        return f"{self.source} declares war on {self.target}" 