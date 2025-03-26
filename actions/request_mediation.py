from actions.base_action import BaseAction
from models.world import World

class RequestMediationAction(BaseAction):
    """Action for requesting mediation from another country."""
    
    def execute(self, world: World) -> bool:
        """Execute the mediation request."""
        if not self.target:
            return False
            
        # Add the event
        world.add_event(f"{self.source} requests mediation from {self.target}")
        return True
        
    def get_description(self) -> str:
        return f"{self.source} requests mediation from {self.target}" 