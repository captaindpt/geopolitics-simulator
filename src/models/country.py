from typing import Dict, List, Optional
from .types import (
    RelationType, StateType, ResourceType, EventCategory,
    ResourceLevel, Sentiment, HistoricalEvent
)

class Country:
    def __init__(self, name: str, strength: float, ideology: str):
        self.name = name
        self.strength = strength
        self.ideology = ideology
        self.relationships: Dict[str, RelationType] = {}
        self.state: StateType = "Peace"
        
        # Enhanced state tracking
        self.resources: Dict[ResourceType, ResourceLevel] = {
            "Military": {"value": strength, "trend": 0.0, "last_update": 0},
            "Economic": {"value": strength * 0.8, "trend": 0.0, "last_update": 0},
            "Diplomatic": {"value": strength * 0.6, "trend": 0.0, "last_update": 0},
            "Cultural": {"value": strength * 0.4, "trend": 0.0, "last_update": 0}
        }
        
        self.sentiment: Dict[str, Sentiment] = {}  # country -> sentiment
        self.history: List[HistoricalEvent] = []
        self.population: float = strength * 1000  # Rough population estimate
        self.culture: Dict[str, float] = {
            "nationalism": 0.5,
            "militarism": 0.5,
            "isolationism": 0.5
        }
    
    def set_relationship(self, country_name: str, relationship: RelationType) -> None:
        """Set relationship with another country"""
        if relationship not in ["Ally", "Enemy", "Neutral", "Tense"]:
            raise ValueError(f"Invalid relationship type: {relationship}")
        self.relationships[country_name] = relationship
        
        # Update sentiment when relationship changes
        if country_name not in self.sentiment:
            self.sentiment[country_name] = {
                "value": 0.0,
                "history": [],
                "last_update": 0
            }
            
        # Update sentiment based on relationship
        if relationship == "Ally":
            self.sentiment[country_name]["value"] = 0.8
        elif relationship == "Enemy":
            self.sentiment[country_name]["value"] = -0.8
        elif relationship == "Tense":
            self.sentiment[country_name]["value"] = -0.3
        else:  # Neutral
            self.sentiment[country_name]["value"] = 0.0
            
        self.sentiment[country_name]["history"].append(self.sentiment[country_name]["value"])
        self.sentiment[country_name]["last_update"] = 0  # Will be updated with current turn
    
    def get_relationship(self, country_name: str) -> RelationType:
        """Get relationship with another country"""
        return self.relationships.get(country_name, "Neutral")
    
    def set_state(self, state: StateType) -> None:
        """Set the current state of the country"""
        if state not in ["Peace", "War", "Mobilizing", "Civil Unrest", "Economic Crisis"]:
            raise ValueError(f"Invalid state type: {state}")
        self.state = state
        
        # Update resource trends based on state change
        if state == "War":
            self.resources["Military"]["trend"] = 0.2
            self.resources["Economic"]["trend"] = -0.3
        elif state == "Economic Crisis":
            self.resources["Economic"]["trend"] = -0.5
            self.resources["Diplomatic"]["trend"] = -0.2
        elif state == "Civil Unrest":
            self.resources["Cultural"]["trend"] = -0.4
            self.resources["Economic"]["trend"] = -0.2
        elif state == "Peace":
            self.resources["Economic"]["trend"] = 0.1
            self.resources["Cultural"]["trend"] = 0.1
            
    def update_resources(self, turn: int) -> None:
        """Update resource levels based on trends and current state"""
        for resource_type, level in self.resources.items():
            # Apply trend
            level["value"] = max(0, min(100, level["value"] + level["trend"]))
            level["last_update"] = turn
            
            # Decay trend towards 0
            level["trend"] *= 0.8
            
    def add_historical_event(self, event: HistoricalEvent) -> None:
        """Add a historical event to the country's history"""
        self.history.append(event)
        # Keep only last 50 events
        if len(self.history) > 50:
            self.history = self.history[-50:]
            
    def update_sentiment(self, country_name: str, change: float, turn: int) -> None:
        """Update sentiment towards another country"""
        if country_name not in self.sentiment:
            self.sentiment[country_name] = {
                "value": 0.0,
                "history": [],
                "last_update": 0
            }
            
        sentiment = self.sentiment[country_name]
        sentiment["value"] = max(-1.0, min(1.0, sentiment["value"] + change))
        sentiment["history"].append(sentiment["value"])
        sentiment["last_update"] = turn
        
        # Keep only last 20 sentiment values
        if len(sentiment["history"]) > 20:
            sentiment["history"] = sentiment["history"][-20:]
            
    def get_recent_events(self, num_events: int = 5) -> List[HistoricalEvent]:
        """Get the most recent historical events"""
        return self.history[-num_events:]
        
    def get_sentiment_trend(self, country_name: str) -> float:
        """Get the sentiment trend towards another country"""
        if country_name not in self.sentiment:
            return 0.0
            
        history = self.sentiment[country_name]["history"]
        if len(history) < 2:
            return 0.0
            
        return history[-1] - history[-2]
        
    def generate_description(self) -> str:
        """Generate a semantic description of the country's current state"""
        parts = [
            f"{self.name} is a {self.ideology} nation with {self.strength} strength.",
            f"Current state: {self.state}",
            f"Population: {self.population:,.0f}"
        ]
        
        # Add resource levels
        for resource_type, level in self.resources.items():
            trend_symbol = "↑" if level["trend"] > 0 else "↓" if level["trend"] < 0 else "→"
            parts.append(f"{resource_type}: {level['value']:.1f} {trend_symbol}")
            
        # Add relationships
        allies = [name for name, rel in self.relationships.items() if rel == "Ally"]
        enemies = [name for name, rel in self.relationships.items() if rel == "Enemy"]
        tense = [name for name, rel in self.relationships.items() if rel == "Tense"]
        
        if allies:
            parts.append(f"Allies: {', '.join(allies)}")
        if enemies:
            parts.append(f"Enemies: {', '.join(enemies)}")
        if tense:
            parts.append(f"Tense relations with: {', '.join(tense)}")
            
        # Add recent history
        if self.history:
            parts.append("Recent events:")
            for event in self.history[-3:]:
                parts.append(f"- {event['description']}")
                
        return "\n".join(parts) 