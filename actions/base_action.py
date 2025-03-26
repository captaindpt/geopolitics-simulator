from typing import Optional, Literal
from models.world import World
from models.country import Country
from datetime import datetime, timedelta
from .cooldown import ActionCooldown

ActionType = Literal[
    "DeclareWar",
    "ProposeAlliance",
    "Help",
    "Mobilize",
    "SueForPeace"
]

class BaseAction:
    """Base class for all actions in the simulation."""
    
    def __init__(self, source: str, target: Optional[str] = None):
        self.source = source
        self.target = target
        
    def execute(self, world: World) -> bool:
        """Execute the action in the world. Returns True if successful."""
        raise NotImplementedError("Subclasses must implement execute()")
        
    def get_description(self) -> str:
        """Get a human-readable description of the action."""
        raise NotImplementedError("Subclasses must implement get_description()")
        
    def __str__(self) -> str:
        return self.get_description()

class DeclareWarAction(BaseAction):
    """Action for declaring war on another country."""
    
    def execute(self, world: World) -> bool:
        if not world.cooldown_manager.is_action_available(self.source, 'declare_war'):
            return False
            
        world.add_conflict(self.source, self.target)
        world.update_relationship(self.source, self.target, -50)
        world.cooldown_manager.record_action(self.source, 'declare_war')
        return True

class ProposeAllianceAction(BaseAction):
    """Action to propose an alliance with another country."""
    
    def execute(self, world) -> bool:
        """Execute alliance proposal."""
        if self.source not in world.countries or self.target not in world.countries:
            return False
            
        source_country = world.countries[self.source]
        target_country = world.countries[self.target]
        
        # Check if alliance would be accepted
        common_enemies = any(
            rel == "Enemy" and target_country.get_relationship(country) == "Enemy"
            for country, rel in source_country.relationships.items()
        )
        
        if common_enemies or target_country.ideology == source_country.ideology:
            # Accept alliance
            source_country.set_relationship(self.target, "Ally")
            target_country.set_relationship(self.source, "Ally")
            
            # Update sentiments positively
            source_country.update_sentiment(self.target, 0.3)
            target_country.update_sentiment(self.source, 0.3)
            
            # Add alliance
            world.add_alliance(
                members=[self.source, self.target],
                strength=0.6,
                type_="Military"
            )
            
            return True
            
        return False

class HelpAction(BaseAction):
    """Action to help another country."""
    
    def execute(self, world) -> bool:
        """Execute help action."""
        if self.source not in world.countries or self.target not in world.countries:
            return False
            
        source_country = world.countries[self.source]
        target_country = world.countries[self.target]
        
        # Transfer some resources
        aid_amount = source_country.resources["economic"] * 0.1
        source_country.update_resources("economic", -aid_amount)
        target_country.update_resources("economic", aid_amount)
        
        # Improve relationship
        target_country.update_sentiment(self.source, 0.2)
        
        if target_country.get_relationship(self.source) == "Neutral":
            target_country.set_relationship(self.source, "Ally")
            source_country.set_relationship(self.target, "Ally")
        
        return True

class MobilizeAction(BaseAction):
    """Action for mobilizing forces."""
    
    def execute(self, world: World) -> bool:
        if not world.cooldown_manager.is_action_available(self.source, 'mobilize'):
            return False
            
        world.countries[self.source].mobilize()
        world.cooldown_manager.record_action(self.source, 'mobilize')
        return True

class SueForPeaceAction(BaseAction):
    """Action to sue for peace with another country."""
    
    def execute(self, world) -> bool:
        """Execute peace proposal."""
        if self.source not in world.countries or self.target not in world.countries:
            return False
            
        source_country = world.countries[self.source]
        target_country = world.countries[self.target]
        
        # Check if peace proposal would be accepted
        if target_country.get_relationship(self.source) == "Enemy":
            # Accept peace proposal
            source_country.set_relationship(self.target, "Neutral")
            target_country.set_relationship(self.source, "Neutral")
            
            # Update sentiments positively
            source_country.update_sentiment(self.target, 0.3)
            target_country.update_sentiment(self.source, 0.3)
            
            # Remove conflict
            world.remove_conflict(
                participants=[self.source, self.target],
                type_="War"
            )
            
            return True
            
        return False

class IssueUltimatumAction(BaseAction):
    """Action for issuing an ultimatum to another country."""
    
    def execute(self, world: World) -> bool:
        if not world.cooldown_manager.is_action_available(self.source, 'issue_ultimatum'):
            return False
            
        world.add_event(f"{self.source} issues ultimatum to {self.target}")
        world.update_relationship(self.source, self.target, -30)
        world.cooldown_manager.record_action(self.source, 'issue_ultimatum')
        return True

class OfferConcessionsAction(BaseAction):
    """Action for offering concessions to another country."""
    
    def execute(self, world: World) -> bool:
        if not world.cooldown_manager.is_action_available(self.source, 'offer_concessions'):
            return False
            
        world.add_event(f"{self.source} offers concessions to {self.target}")
        world.update_relationship(self.source, self.target, 20)
        world.cooldown_manager.record_action(self.source, 'offer_concessions')
        return True

class RequestMediationAction(BaseAction):
    """Action for requesting mediation from another country."""
    
    def execute(self, world: World) -> bool:
        if not world.cooldown_manager.is_action_available(self.source, 'request_mediation'):
            return False
            
        world.add_event(f"{self.source} requests mediation from {self.target}")
        world.update_relationship(self.source, self.target, 10)
        world.cooldown_manager.record_action(self.source, 'request_mediation')
        return True 