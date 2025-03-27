from typing import List, Optional, TYPE_CHECKING
from src.models.world import World
from src.models.country import Country
from src.models.types import StateType

if TYPE_CHECKING:
    from src.models.world import World

class Agent:
    def __init__(self, country_name: str, personality: str):
        """
        Initialize an agent for a country
        
        Args:
            country_name: Name of the country this agent controls
            personality: "Aggressive", "Cautious", or "Neutral"
        """
        self.country_name = country_name
        if personality not in ["Aggressive", "Cautious", "Neutral"]:
            raise ValueError(f"Invalid personality type: {personality}")
        self.personality = personality
        self.memory: List[str] = []  # List of events agent remembers
        
    def perceive(self, world: World) -> str:
        """
        Create a text description of what agent perceives
        
        Args:
            world: Current world state
            
        Returns:
            String description of agent's perception
        """
        country = world.get_country(self.country_name)
        if not country:
            raise ValueError(f"Country {self.country_name} not found in world")
            
        perception = self._build_perception(world, country)
        self._update_memory(world)
        return perception
        
    def _build_perception(self, world: World, country: Country) -> str:
        """Build the perception string from world state"""
        parts = [
            f"I am the leader of {self.country_name}, which is {country.ideology}.",
            f"We are currently in a state of {country.state}."
        ]
        
        # Add relationships
        allies = [name for name, relation in country.relationships.items() 
                 if relation == "Ally"]
        enemies = [name for name, relation in country.relationships.items() 
                  if relation == "Enemy"]
        
        if allies:
            parts.append(f"Our allies are {', '.join(allies)}.")
        if enemies:
            parts.append(f"We are Enemy with {', '.join(enemies)}.")
            
        # Add recent events
        if world.events:
            parts.append("Recent events:")
            # Get last 3 events
            for event in world.events[-3:]:
                parts.append(f"- {event['text']}")
                
        return " ".join(parts)
        
    def _update_memory(self, world: World) -> None:
        """Update agent's memory with recent events"""
        if world.events:
            new_events = [e['text'] for e in world.events[-3:]]
            self.memory.extend(new_events)
            # Keep only last 10 memories
            self.memory = self.memory[-10:]
    
    def decide(self, world: World) -> str:
        """
        Make a decision based on current world state
        
        Args:
            world: Current world state
            
        Returns:
            Decision string describing chosen action
        """
        country = world.get_country(self.country_name)
        if not country:
            return "Do nothing"
            
        decisions = self._generate_decisions(world, country)
        return decisions[0] if decisions else "Do nothing"
        
    def _generate_decisions(self, world: World, country: Country) -> List[str]:
        """Generate possible decisions based on personality and state"""
        decisions = []
        
        # Rule 1: If at peace and aggressive, look for weak enemies
        if (country.state == "Peace" and 
            self.personality == "Aggressive"):
            for name, other in world.countries.items():
                if (name != self.country_name and 
                    country.get_relationship(name) == "Neutral" and
                    country.strength > other.strength * 1.5):
                    decisions.append(f"Declare war on {name}")
        
        # Rule 2: If at war and losing, seek allies
        if country.state == "War":
            enemies = [name for name, rel in country.relationships.items() 
                      if rel == "Enemy"]
            enemy_strength = sum(world.countries[name].strength 
                               for name in enemies)
            
            if enemy_strength > country.strength:
                for name, other in world.countries.items():
                    if (name != self.country_name and
                        country.get_relationship(name) == "Neutral" and
                        other.ideology == country.ideology):
                        decisions.append(f"Propose alliance to {name}")
        
        # Rule 3: Help allies in war if not cautious
        if country.state == "Peace" and self.personality != "Cautious":
            for name, other in world.countries.items():
                if (other.ideology == country.ideology and 
                    other.state == "War" and
                    country.get_relationship(name) == "Neutral"):
                    decisions.append(f"Help {name}")
        
        return decisions 

    def make_decision(self, world: 'World') -> Optional[str]:
        """
        Make a decision based on the current world state
        
        Args:
            world: The current world state
            
        Returns:
            Optional[str]: The decision made by the agent, or None if no action is taken
        """
        # Basic decision-making logic based on behavior
        if self.personality == "Aggressive":
            # Look for enemies to declare war on
            for country_name, country in world.countries.items():
                if country_name != self.country_name:
                    relationships = world.countries[self.country_name].relationships
                    if country_name in relationships and relationships[country_name] == "Enemy":
                        return f"Declare war on {country_name}"
        
        elif self.personality == "Cautious":
            # Look for allies when at war
            if world.countries[self.country_name].state == "War":
                for country_name, country in world.countries.items():
                    if country_name != self.country_name:
                        relationships = world.countries[self.country_name].relationships
                        if country_name not in relationships:
                            return f"Propose alliance with {country_name}"
        
        # Default: do nothing
        return None 