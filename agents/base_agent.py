from enum import Enum
from typing import List, Literal, Optional, Dict
from models.world import World
from actions.action_factory import ActionFactory
from actions.base_action import BaseAction

class PersonalityType(Enum):
    AGGRESSIVE = "aggressive"
    DIPLOMATIC = "diplomatic"
    CAUTIOUS = "cautious"
    OPPORTUNISTIC = "opportunistic"

class Agent:
    """
    Base agent class that makes decisions for a country based on personality and world state.
    """
    def __init__(self, name: str, personality: PersonalityType):
        self.name = name
        self.personality = personality
        self.memory: List[str] = []  # List of important events agent remembers
        
    def perceive(self, world: World) -> str:
        """
        Create a text description of what the agent perceives about the world state.
        """
        country = world.get_country(self.name)
        
        # Build perception text
        perception = [
            f"I am the leader of {self.name}, which is {country.ideology}.",
            f"We are currently in a state of {country.state}."
        ]
        
        # Add relationship information
        allies = [name for name, relation in country.relationships.items() 
                 if relation == "Ally"]
        enemies = [name for name, relation in country.relationships.items() 
                  if relation == "Enemy"]
        
        if allies:
            perception.append(f"Our allies are {', '.join(allies)}.")
        if enemies:
            perception.append(f"Our enemies are {', '.join(enemies)}.")
            
        # Add recent events
        if world.events:
            perception.append("Recent events:")
            # Get last 3 events
            for event in world.events[-3:]:
                perception.append(f"- {event['text']}")
                
        return " ".join(perception)
        
    def _make_decision(self, world: World) -> str:
        """
        Internal method to make a decision based on personality and current world state.
        Returns a decision string that can be converted into an action.
        """
        country = world.get_country(self.name)
        decisions = []
        
        # Rule 1: Aggressive personality looks for opportunities to attack
        if self.personality == PersonalityType.AGGRESSIVE and country.state == "Peace":
            for name, other in world.countries.items():
                if (name != self.name and 
                    country.get_relationship(name) == "Neutral" and
                    country.strength > other.strength * 1.5):
                    decisions.append(f"Declare war on {name}")
        
        # Rule 2: All personalities seek allies when at war and outnumbered
        if country.state == "War":
            enemies = [name for name, rel in country.relationships.items() 
                      if rel == "Enemy"]
            enemy_strength = sum(world.get_country(name).strength 
                               for name in enemies)
            
            if enemy_strength > country.strength:
                for name, other in world.countries.items():
                    if (name != self.name and 
                        country.get_relationship(name) == "Neutral" and
                        other.ideology == country.ideology):
                        decisions.append(f"Propose alliance to {name}")
        
        # Rule 3: Non-cautious personalities may help allies
        if (self.personality != PersonalityType.CAUTIOUS and 
            country.state == "Peace"):
            for name, other in world.countries.items():
                if (other.ideology == country.ideology and 
                    other.state == "War" and
                    country.get_relationship(name) == "Neutral"):
                    decisions.append(f"Help {name}")
        
        return decisions[0] if decisions else "Do nothing"

    def decide(self, world: World) -> Optional[BaseAction]:
        """
        Make a decision and return an Action object (or None for no action).
        """
        perception = self.perceive(world)
        decision = self._make_decision(world)
        return ActionFactory.create_action(decision, self.name)

    def _generate_perception(self, world: World) -> Dict:
        """Generate a perception of the world state."""
        return {
            "global_tension": world.global_tension,
            "active_conflicts": list(world.active_conflicts),
            "recent_events": world.events[-5:] if world.events else [],
            "allies": list(world.get_allies(self.name)),
            "enemies": list(world.get_enemies(self.name))
        } 