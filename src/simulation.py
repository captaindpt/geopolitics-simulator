from typing import Dict, List, Optional
from .llm import LLMClient

class Simulation:
    def __init__(self, llm: LLMClient):
        self.llm = llm
        self.world_state = {
            "turn": 1,
            "countries": {},
            "events": [],
            "global_state": {
                "tension": 0.5,
                "economic_health": 0.5,
                "military_balance": 0.5
            }
        }
        
    def add_country(self, name: str, profile: Dict):
        """Add a country to the simulation"""
        self.world_state["countries"][name] = {
            "name": name,
            "ideology": profile["ideology"],
            "personality": profile["personality"],
            "strength": profile["strength"],
            "state": "Peace",
            "relationships": {},
            "resources": {
                "military": profile["strength"],
                "economic": profile["strength"] * 0.8,
                "diplomatic": profile["strength"] * 0.6
            }
        }
        
        # Set up relationships
        for ally in profile.get("allies", []):
            if ally in self.world_state["countries"]:
                self.world_state["countries"][name]["relationships"][ally] = "ally"
                self.world_state["countries"][ally]["relationships"][name] = "ally"
                
        for enemy in profile.get("enemies", []):
            if enemy in self.world_state["countries"]:
                self.world_state["countries"][name]["relationships"][enemy] = "enemy"
                self.world_state["countries"][enemy]["relationships"][name] = "enemy"
                
    def add_event(self, event: Dict):
        """Add an event to the simulation"""
        event["turn"] = self.world_state["turn"]
        self.world_state["events"].append(event)
        
        # Update affected countries
        for country, impact in event.get("impact", {}).items():
            if country in self.world_state["countries"]:
                # Update resources based on impact
                for resource in self.world_state["countries"][country]["resources"]:
                    self.world_state["countries"][country]["resources"][resource] *= (1 + impact)
                    
    def run(self, turns: int = 10) -> List[Dict]:
        """Run the simulation for a specified number of turns"""
        history = []
        
        for _ in range(turns):
            # Get decisions from all countries
            actions = []
            for country_name, country in self.world_state["countries"].items():
                decision = self.llm.get_country_decision(
                    country_name=country_name,
                    personality=country["personality"],
                    world_state=self.world_state,
                    recent_events=self.world_state["events"][-5:]  # Last 5 events
                )
                
                actions.append({
                    "country": country_name,
                    "text": decision
                })
            
            # Resolve conflicts and get outcomes
            resolved_actions = self.llm.resolve_conflicts(
                actions=actions,
                world_state=self.world_state
            )
            
            # Apply resolved actions
            for action in resolved_actions:
                self.add_event({
                    "text": action["text"],
                    "impact": self._calculate_impact(action)
                })
            
            # Save turn state to history
            history.append({
                "turn": self.world_state["turn"],
                "events": self.world_state["events"][-len(resolved_actions):],
                "countries": {
                    name: {
                        "state": country["state"],
                        "resources": dict(country["resources"])
                    }
                    for name, country in self.world_state["countries"].items()
                }
            })
            
            # Advance turn
            self.world_state["turn"] += 1
            
        return history
    
    def _calculate_impact(self, action: Dict) -> Dict[str, float]:
        """Calculate the impact of an action on different countries"""
        # This would be a more sophisticated calculation based on the action
        # For now, return a simple impact
        return {
            "global": -0.1  # Slight negative impact on global stability
        } 