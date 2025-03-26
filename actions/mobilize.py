from actions.base_action import BaseAction
from models.world import World

class MobilizeAction(BaseAction):
    """Action for mobilizing forces."""
    
    def execute(self, world: World) -> bool:
        """Execute the mobilization."""
        # Add the event
        world.add_event(f"{self.source} mobilizes its forces")
        return True
        
    def get_description(self) -> str:
        return f"{self.source} mobilizes its forces" 