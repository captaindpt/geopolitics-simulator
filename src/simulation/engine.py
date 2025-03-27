from __future__ import annotations
from typing import Dict, List, Optional, Callable, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from src.models.world import World

class SimulationEngine:
    def __init__(self, world: World):
        """
        Initialize simulation engine
        
        Args:
            world: The world state to simulate
        """
        self.world = world
        self.history: List[Dict[str, Any]] = []  # List of world state snapshots
        self.should_stop = False
        
    def run_turn(self) -> List[str]:
        """Execute a single turn of the simulation"""
        # Get decisions from all agents
        actions = []
        for agent in self.world.agents.values():
            decision = agent.decide(self.world)
            if decision and decision != "Do nothing":
                # Execute the action
                if self.world.execute_action(decision):
                    actions.append(decision)
        
        # Save snapshot before advancing turn
        snapshot = self._get_world_state(actions)
        self.history.append(snapshot)
        
        # Advance turn after saving snapshot
        self.world.advance_turn()
        
        return actions
        
    def run_simulation(self, num_turns: int) -> List[Dict[str, Any]]:
        """Run the simulation for a specified number of turns"""
        if self.should_stop:
            return []
            
        history = []
        
        for _ in range(num_turns):
            if self.should_stop:
                break
                
            actions = self.run_turn()
            history.append(self.history[-1])  # Use the last saved snapshot
        
        return history
        
    def stop(self) -> None:
        """Stop the simulation"""
        self.should_stop = True
        
    def _get_world_state(self, actions: List[str]) -> Dict[str, Any]:
        """Get the current world state as a dictionary"""
        return {
            "turn": self.world.turn,
            "actions": actions,
            "countries": {
                name: {
                    "name": country.name,
                    "strength": country.strength,
                    "ideology": country.ideology,
                    "state": country.state,
                    "relationships": country.relationships
                }
                for name, country in self.world.countries.items()
            },
            "events": self.world.events
        } 