from typing import Dict, List, Any, Optional
from src.models.world import World
from src.models.country import Country
from src.agents.llm_agent import LLMAgent
from src.config.llm_config import LLMConfig
import os

class Simulation:
    def __init__(self, llm_client):
        """Initialize simulation with LLM client"""
        self.world = World()
        self.llm_client = llm_client
        self.history: List[Dict[str, Any]] = []
        
    def add_country(self, name: str, profile: Dict[str, Any]) -> None:
        """Add a country with its profile to the simulation"""
        # Create country
        country = Country(
            name=name,
            strength=profile["strength"],
            ideology=profile["ideology"]
        )
        self.world.add_country(country)
        
        # Create agent
        agent = LLMAgent(
            country_name=name,
            personality=profile["personality"],
            api_key=os.getenv("HUGGINGFACE_API_KEY"),
            config=LLMConfig()
        )
        self.world.add_agent(agent)
        
        # Set relationships
        for ally in profile.get("allies", []):
            if ally in self.world.countries:
                country.set_relationship(ally, "Ally")
                self.world.countries[ally].set_relationship(name, "Ally")
                
        for enemy in profile.get("enemies", []):
            if enemy in self.world.countries:
                country.set_relationship(enemy, "Enemy")
                self.world.countries[enemy].set_relationship(name, "Enemy")
                
    def add_event(self, event: Dict[str, Any]) -> None:
        """Add an event to the simulation"""
        self.world.add_event(event)
        
    def _save_world_state(self, actions: List[str]) -> None:
        """Save the current world state to history"""
        state = {
            "turn": self.world.turn,
            "actions": actions,
            "events": self.world.events[-3:],  # Last 3 events
            "countries": {
                name: {
                    "name": country.name,
                    "strength": country.strength,
                    "ideology": country.ideology,
                    "state": country.state,
                    "relationships": dict(country.relationships)
                }
                for name, country in self.world.countries.items()
            }
        }
        self.history.append(state)
        
    def run(self, turns: int = 10) -> List[Dict[str, Any]]:
        """Run the simulation for specified number of turns"""
        for _ in range(turns):
            # Get decisions from all agents
            actions = self.world.run_agent_turns()
            
            # Save world state
            self._save_world_state(actions)
            
            # Advance turn
            self.world.advance_turn()
            
        # Print final results
        print("\nSimulation Results:")
        for state in self.history:
            print(f"\nTurn {state['turn']}:")
            if state['events']:
                print("Events:")
                for event in state['events']:
                    print(f"- {event['text']}")
            if state['actions']:
                print("\nActions:")
                for action in state['actions']:
                    print(f"- {action}")
            print("\nWorld State:")
            for name, country in state['countries'].items():
                status = f"{name}: {country['state']}"
                if country['state'] == "War":
                    enemies = [c for c, r in country['relationships'].items() 
                             if r == "Enemy"]
                    if enemies:
                        status += f" (at war with {', '.join(enemies)})"
                print(status)
                
        return self.history 