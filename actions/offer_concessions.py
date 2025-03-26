from actions.base_action import BaseAction
from models.world import World

class OfferConcessionsAction(BaseAction):
    """Action for offering concessions to another country."""
    
    def execute(self, world: World) -> bool:
        """Execute the concessions offer."""
        if not self.target:
            return False
            
        # Add the event
        world.add_event(f"{self.source} offers concessions to {self.target}")
        return True
        
    def get_description(self) -> str:
        return f"{self.source} offers concessions to {self.target}" 