from __future__ import annotations
from typing import Dict, List, Optional, TYPE_CHECKING, Any
from datetime import datetime

from .country import Country
from .types import Event, EventCategory, HistoricalEvent
from src.actions.action_factory import ActionFactory

if TYPE_CHECKING:
    from src.agents.base_agent import Agent
    from src.actions.base_action import Action

class World:
    def __init__(self) -> None:
        self.countries: Dict[str, Country] = {}
        self.agents: Dict[str, Agent] = {}  # country_name -> Agent
        self.turn: int = 0
        self.events: List[Dict[str, Any]] = []
        self.global_resources: Dict[str, float] = {
            "oil": 100.0,
            "food": 100.0,
            "technology": 100.0
        }
        self.global_trends: Dict[str, float] = {
            "globalization": 0.5,
            "militarization": 0.5,
            "economic_growth": 0.5
        }
        self.start_date = datetime.now()
        self.narrative_context: Dict[str, Any] = {
            "historical_events": [],
            "current_tensions": [],
            "diplomatic_relations": {},
            "economic_conditions": {},
            "public_sentiment": {}
        }
    
    def add_country(self, country: Country) -> None:
        """Add a country to the world"""
        self.countries[country.name] = country
        self.narrative_context["diplomatic_relations"][country.name] = {}
        self.narrative_context["economic_conditions"][country.name] = "stable"
        self.narrative_context["public_sentiment"][country.name] = "neutral"
    
    def get_country(self, name: str) -> Optional[Country]:
        """Get a country by name"""
        return self.countries.get(name)
    
    def add_agent(self, agent: Agent) -> None:
        """Add an agent to the world"""
        self.agents[agent.country_name] = agent
    
    def get_agent(self, country_name: str) -> Optional[Agent]:
        """Get an agent by country name"""
        return self.agents.get(country_name)
    
    def set_relationship(self, country1: str, country2: str, relationship: str) -> None:
        """Set relationship between two countries"""
        if country1 in self.countries and country2 in self.countries:
            if country1 == country2:
                return
                
            if (self.countries[country1].get_relationship(country2) == "Enemy" and
                relationship != "Enemy"):
                return
                
            self.countries[country1].set_relationship(country2, relationship)
            self.countries[country2].set_relationship(country1, relationship)
            
            # Update narrative context
            self.narrative_context["diplomatic_relations"][country1][country2] = relationship
            self.narrative_context["diplomatic_relations"][country2][country1] = relationship
            
            # Generate narrative event for significant relationship changes
            if relationship in ["Ally", "Enemy"]:
                event_text = self._generate_relationship_narrative(country1, country2, relationship)
                self.add_event({
                    "text": event_text,
                    "category": "Diplomatic",
                    "impact": {
                        country1: 0.1 if relationship == "Ally" else -0.2,
                        country2: 0.1 if relationship == "Ally" else -0.2
                    },
                    "affected_countries": [country1, country2],
                    "narrative": event_text
                })
    
    def _generate_relationship_narrative(self, country1: str, country2: str, relationship: str) -> str:
        """Generate a narrative description of a relationship change"""
        if relationship == "Ally":
            return f"In a significant diplomatic development, {country1} and {country2} have formed a strategic alliance. This partnership marks a new chapter in their relations, with both nations pledging mutual support and cooperation."
        else:  # Enemy
            return f"Tensions have reached a breaking point as {country1} and {country2} have declared each other as enemies. This dramatic shift in relations has sent shockwaves through the international community."
    
    def execute_action(self, action: Dict[str, Any]) -> bool:
        """Execute an action in the world"""
        source_country = None
        for agent in self.agents.values():
            if agent.country_name in action["narrative"]:
                source_country = agent.country_name
                break
                
        if source_country:
            country = self.countries[source_country]
            
            if country.state == "War" and action["action"] == "Declare war":
                return False
                
            action_obj = ActionFactory.create_action(action["action"], source_country)
            if action_obj:
                success = action_obj.execute(self)
                if success:
                    # Add narrative event
                    self.add_event({
                        "text": action["narrative"],
                        "category": "Military" if "war" in action["action"].lower() else "Diplomatic",
                        "impact": {},
                        "affected_countries": [source_country],
                        "narrative": action["narrative"]
                    })
                return success
        return False
    
    def advance_turn(self) -> None:
        """Advance to the next turn"""
        self.turn += 1
        
        # Update all countries' resources
        for country in self.countries.values():
            country.update_resources(self.turn)
            
        # Update global trends
        self._update_global_trends()
        
        # Generate turn narrative
        at_war = [name for name, country in self.countries.items() 
                 if country.state == "War"]
        if at_war:
            war_narrative = self._generate_war_narrative(at_war)
            self.add_event({
                "text": f"Turn {self.turn}: {len(at_war)} countries at war",
                "category": "Military",
                "impact": {},
                "affected_countries": at_war,
                "narrative": war_narrative
            })
    
    def _update_global_trends(self) -> None:
        """Update global trends based on current world state"""
        # Count wars and alliances
        war_count = sum(1 for c in self.countries.values() if c.state == "War")
        alliance_count = sum(
            sum(1 for r in c.relationships.values() if r == "Ally")
            for c in self.countries.values()
        ) // 2  # Divide by 2 since each alliance is counted twice
        
        # Update trends based on counts
        self.global_trends["militarization"] = min(1.0, max(0.0,
            self.global_trends["militarization"] + (war_count * 0.1)))
        self.global_trends["globalization"] = min(1.0, max(0.0,
            self.global_trends["globalization"] + (alliance_count * 0.05)))
            
        # Economic growth based on peace/war ratio
        peace_count = sum(1 for c in self.countries.values() if c.state == "Peace")
        total_countries = len(self.countries)
        peace_ratio = peace_count / total_countries if total_countries > 0 else 0.5
        
        self.global_trends["economic_growth"] = min(1.0, max(0.0,
            self.global_trends["economic_growth"] + (peace_ratio - 0.5) * 0.1))
    
    def _update_global_trends_from_event(self, event: HistoricalEvent) -> None:
        """Update global trends based on event category"""
        if event["category"] == "Military":
            self.global_trends["militarization"] = min(1.0, max(0.0,
                self.global_trends["militarization"] + 0.1))
        elif event["category"] == "Diplomatic":
            self.global_trends["globalization"] = min(1.0, max(0.0,
                self.global_trends["globalization"] + 0.05))
        elif event["category"] == "Economic":
            self.global_trends["economic_growth"] = min(1.0, max(0.0,
                self.global_trends["economic_growth"] + 0.05))
    
    def _generate_war_narrative(self, countries: List[str]) -> str:
        """Generate a narrative description of the current war situation"""
        if len(countries) == 1:
            return f"The conflict continues as {countries[0]} remains embroiled in war, with its people and resources strained by the ongoing hostilities."
        elif len(countries) == 2:
            return f"The war between {countries[0]} and {countries[1]} rages on, with both nations locked in a bitter struggle for supremacy."
        else:
            return f"The world finds itself in the midst of a complex multi-nation conflict, with {', '.join(countries[:-1])}, and {countries[-1]} all engaged in hostilities. The international community watches with growing concern as the war's impact spreads far beyond the battlefield."
    
    def add_event(self, event: Dict[str, Any]) -> None:
        """Add an event to the world history"""
        event["turn"] = self.turn
        self.events.append(event)
        
        # Create historical event
        historical_event: HistoricalEvent = {
            "turn": self.turn,
            "category": event.get("category", "Internal"),
            "description": event.get("narrative", event["text"]),
            "impact": event.get("impact", {}),
            "related_events": event.get("related_events", [])
        }
        
        # Add to affected countries' histories
        affected_countries = event.get("affected_countries", [])
        for country_name in affected_countries:
            if country_name in self.countries:
                self.countries[country_name].add_historical_event(historical_event)
                
        # Update global trends based on event category
        self._update_global_trends_from_event(historical_event)
        
        # Update narrative context
        self._update_narrative_context(event)
    
    def _update_narrative_context(self, event: Dict[str, Any]) -> None:
        """Update the narrative context based on new events"""
        # Add to historical events
        self.narrative_context["historical_events"].append({
            "turn": event["turn"],
            "description": event.get("narrative", event["text"]),
            "category": event.get("category", "Internal")
        })
        
        # Keep only last 20 historical events
        if len(self.narrative_context["historical_events"]) > 20:
            self.narrative_context["historical_events"] = self.narrative_context["historical_events"][-20:]
        
        # Update current tensions
        if event.get("category") == "Military":
            self.narrative_context["current_tensions"].append({
                "turn": event["turn"],
                "description": event.get("narrative", event["text"]),
                "countries": event.get("affected_countries", [])
            })
        
        # Keep only last 5 tensions
        if len(self.narrative_context["current_tensions"]) > 5:
            self.narrative_context["current_tensions"] = self.narrative_context["current_tensions"][-5:]
    
    def get_world_state(self) -> Dict[str, Any]:
        """Get current world state as a dictionary"""
        return {
            "turn": self.turn,
            "countries": {
                name: {
                    "name": country.name,
                    "strength": country.strength,
                    "ideology": country.ideology,
                    "state": country.state,
                    "relationships": country.relationships,
                    "resources": country.resources,
                    "population": country.population,
                    "culture": country.culture
                }
                for name, country in self.countries.items()
            },
            "global_resources": self.global_resources,
            "global_trends": self.global_trends,
            "events": self.events[-10:],  # Last 10 events
            "narrative_context": self.narrative_context
        }
    
    def run_agent_turns(self) -> List[Dict[str, Any]]:
        """
        Run all agents for one turn and execute their decisions
        
        Returns:
            List of executed action descriptions with narratives
        """
        executed_actions = []
        for agent in self.agents.values():
            decision = agent.decide(self)
            if decision["action"] != "Do nothing":
                # Execute the action
                if self.execute_action(decision):
                    executed_actions.append(decision)
        
        return executed_actions 