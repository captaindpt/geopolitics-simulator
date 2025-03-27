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
            },
            "narrative_context": {
                "historical_events": [],
                "current_tensions": [],
                "diplomatic_relations": {},
                "economic_conditions": {},
                "public_sentiment": {}
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
        
        # Initialize narrative context for the country
        self.world_state["narrative_context"]["diplomatic_relations"][name] = {}
        self.world_state["narrative_context"]["economic_conditions"][name] = "stable"
        self.world_state["narrative_context"]["public_sentiment"][name] = "neutral"
        
        # Set up relationships
        for ally in profile.get("allies", []):
            if ally in self.world_state["countries"]:
                self.world_state["countries"][name]["relationships"][ally] = "ally"
                self.world_state["countries"][ally]["relationships"][name] = "ally"
                self._update_relationship_narrative(name, ally, "ally")
                
        for enemy in profile.get("enemies", []):
            if enemy in self.world_state["countries"]:
                self.world_state["countries"][name]["relationships"][enemy] = "enemy"
                self.world_state["countries"][enemy]["relationships"][name] = "enemy"
                self._update_relationship_narrative(name, enemy, "enemy")
                
    def _update_relationship_narrative(self, country1: str, country2: str, relationship: str):
        """Update narrative context for relationship changes"""
        self.world_state["narrative_context"]["diplomatic_relations"][country1][country2] = relationship
        self.world_state["narrative_context"]["diplomatic_relations"][country2][country1] = relationship
        
        # Generate narrative for significant relationship changes
        if relationship in ["ally", "enemy"]:
            narrative = (
                f"In a significant diplomatic development, {country1} and {country2} have formed a strategic alliance. "
                f"This partnership marks a new chapter in their relations, with both nations pledging mutual support and cooperation."
                if relationship == "ally"
                else f"Tensions have reached a breaking point as {country1} and {country2} have declared each other as enemies. "
                     f"This dramatic shift in relations has sent shockwaves through the international community."
            )
            
            self.add_event({
                "text": f"{country1} and {country2} became {relationship}s",
                "narrative": narrative,
                "impact": {
                    country1: 0.1 if relationship == "ally" else -0.2,
                    country2: 0.1 if relationship == "ally" else -0.2
                }
            })
                
    def add_event(self, event: Dict):
        """Add an event to the simulation"""
        event["turn"] = self.world_state["turn"]
        self.world_state["events"].append(event)
        
        # Update narrative context
        self._update_narrative_context(event)
        
        # Update affected countries
        for country, impact in event.get("impact", {}).items():
            if country in self.world_state["countries"]:
                # Update resources based on impact
                for resource in self.world_state["countries"][country]["resources"]:
                    self.world_state["countries"][country]["resources"][resource] *= (1 + impact)
                    
    def _update_narrative_context(self, event: Dict):
        """Update the narrative context based on new events"""
        # Add to historical events
        self.world_state["narrative_context"]["historical_events"].append({
            "turn": event["turn"],
            "description": event.get("narrative", event["text"]),
            "category": event.get("category", "Internal")
        })
        
        # Keep only last 20 historical events
        if len(self.world_state["narrative_context"]["historical_events"]) > 20:
            self.world_state["narrative_context"]["historical_events"] = (
                self.world_state["narrative_context"]["historical_events"][-20:]
            )
        
        # Update current tensions for military events
        if event.get("category") == "Military":
            self.world_state["narrative_context"]["current_tensions"].append({
                "turn": event["turn"],
                "description": event.get("narrative", event["text"]),
                "countries": event.get("affected_countries", [])
            })
            
            # Keep only last 5 tensions
            if len(self.world_state["narrative_context"]["current_tensions"]) > 5:
                self.world_state["narrative_context"]["current_tensions"] = (
                    self.world_state["narrative_context"]["current_tensions"][-5:]
                )
                    
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
                    "action": decision["action"],
                    "narrative": decision["narrative"]
                })
            
            # Resolve conflicts and get outcomes
            resolved_actions = self.llm.resolve_conflicts(
                actions=actions,
                world_state=self.world_state
            )
            
            # Apply resolved actions
            for action in resolved_actions:
                self.add_event({
                    "text": action["action"],
                    "narrative": action["narrative"],
                    "impact": self._calculate_impact(action)
                })
            
            # Generate turn narrative
            turn_narrative = self._generate_turn_narrative()
            
            # Save turn state to history
            history.append({
                "turn": self.world_state["turn"],
                "narrative": turn_narrative,
                "events": self.world_state["events"][-len(resolved_actions):],
                "countries": {
                    name: {
                        "state": country["state"],
                        "resources": dict(country["resources"]),
                        "narrative": self._generate_country_narrative(name, country)
                    }
                    for name, country in self.world_state["countries"].items()
                }
            })
            
            # Advance turn
            self.world_state["turn"] += 1
            
        return history
    
    def _generate_turn_narrative(self) -> str:
        """Generate a narrative summary of the current turn"""
        at_war = [name for name, country in self.world_state["countries"].items() 
                 if country["state"] == "War"]
        
        if at_war:
            if len(at_war) == 1:
                return f"The conflict continues as {at_war[0]} remains embroiled in war, with its people and resources strained by the ongoing hostilities."
            elif len(at_war) == 2:
                return f"The war between {at_war[0]} and {at_war[1]} rages on, with both nations locked in a bitter struggle for supremacy."
            else:
                return f"The world finds itself in the midst of a complex multi-nation conflict, with {', '.join(at_war[:-1])}, and {at_war[-1]} all engaged in hostilities. The international community watches with growing concern as the war's impact spreads far beyond the battlefield."
        else:
            return "The world enjoys a period of relative peace, though diplomatic tensions remain high as nations carefully watch each other's movements."
    
    def _generate_country_narrative(self, name: str, country: Dict) -> str:
        """Generate a narrative description of a country's current state"""
        parts = [
            f"{name} stands as a {country['ideology']} nation with significant {country['strength']} strength.",
            f"Currently in a state of {country['state']}, the nation's resources reflect its position:"
        ]
        
        # Add resource levels with trends
        for resource, value in country["resources"].items():
            trend = "increasing" if value > country["strength"] else "decreasing" if value < country["strength"] else "stable"
            parts.append(f"- {resource}: {value:.1f} ({trend})")
        
        # Add relationships
        allies = [c for c, r in country["relationships"].items() if r == "ally"]
        enemies = [c for c, r in country["relationships"].items() if r == "enemy"]
        
        if allies:
            parts.append(f"The nation maintains strong alliances with {', '.join(allies)}.")
        if enemies:
            parts.append(f"Tensions remain high with {', '.join(enemies)}.")
            
        return " ".join(parts)
    
    def _calculate_impact(self, action: Dict) -> Dict[str, float]:
        """Calculate the impact of an action on different countries"""
        # This would be a more sophisticated calculation based on the action
        # For now, return a simple impact
        return {
            "global": -0.1  # Slight negative impact on global stability
        } 