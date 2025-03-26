from typing import Optional
from .base_action import Action, ActionType
from models.world import World

class DeclareWarAction(Action):
    def __init__(self, source_country: str, target_country: str):
        super().__init__(
            action_type="DeclareWar",
            source_country=source_country,
            target_country=target_country,
            description=f"{source_country} declares war on {target_country}"
        )

    def execute(self, world: World) -> bool:
        if not self.target_country:
            return False

        source = world.get_country(self.source_country)
        target = world.get_country(self.target_country)

        # Set mutual enemy relationships
        source.set_relationship(self.target_country, "Enemy")
        target.set_relationship(self.source_country, "Enemy")

        # Update states
        source.set_state("War")
        target.set_state("War")

        # Record the event
        world.add_event(self.description)
        return True

class ProposeAllianceAction(Action):
    def __init__(self, source_country: str, target_country: str):
        super().__init__(
            action_type="ProposeAlliance",
            source_country=source_country,
            target_country=target_country,
            description=f"{source_country} proposes alliance to {target_country}"
        )

    def execute(self, world: World) -> bool:
        if not self.target_country:
            return False

        source = world.get_country(self.source_country)
        target = world.get_country(self.target_country)

        # Simple alliance acceptance logic
        will_accept = (
            # Same ideology
            source.ideology == target.ideology or
            # Common enemies
            any(target.get_relationship(country) == "Enemy" 
                for country, relation in source.relationships.items()
                if relation == "Enemy")
        )

        if will_accept:
            source.set_relationship(self.target_country, "Ally")
            target.set_relationship(self.source_country, "Ally")
            world.add_event(f"{self.source_country} and {self.target_country} formed an alliance")
            return True
        else:
            world.add_event(f"{self.target_country} rejected {self.source_country}'s alliance proposal")
            return False

class HelpAction(Action):
    def __init__(self, source_country: str, target_country: str):
        super().__init__(
            action_type="Help",
            source_country=source_country,
            target_country=target_country,
            description=f"{source_country} offers help to {target_country}"
        )

    def execute(self, world: World) -> bool:
        if not self.target_country:
            return False

        target = world.get_country(self.target_country)
        source = world.get_country(self.source_country)

        # Find target's enemies
        enemies = [name for name, relation in target.relationships.items() 
                  if relation == "Enemy"]

        if enemies:
            # Join war against first enemy
            enemy = enemies[0]
            source.set_relationship(enemy, "Enemy")
            world.get_country(enemy).set_relationship(self.source_country, "Enemy")
            source.set_state("War")

            # Become allies with target
            source.set_relationship(self.target_country, "Ally")
            target.set_relationship(self.source_country, "Ally")

            world.add_event(f"{self.source_country} joined {self.target_country} against {enemy}")
            return True

        return False 