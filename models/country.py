from typing import Dict, List, Literal, Optional, Union
from dataclasses import dataclass
from datetime import datetime

RelationType = Literal["Ally", "Enemy", "Neutral"]
StateType = Literal["Peace", "War", "Mobilizing"]

@dataclass
class HistoricalEvent:
    """Represents a significant historical event for a country."""
    timestamp: datetime
    description: str
    impact: float  # -1.0 to 1.0 impact on country
    related_countries: List[str]

class Country:
    """
    Represents a country in the simulation with enhanced state tracking.
    """
    def __init__(self, name: str):
        self.name = name
        self.military_power = 0
        self.economic_power = 0
        self.internal_stability = 100
        self.relationships: Dict[str, int] = {}  # country -> relationship score (-100 to 100)
        self.is_mobilized = False
        
        # Enhanced state tracking
        self.sentiment: Dict[str, float] = {}  # Country -> sentiment (-1.0 to 1.0)
        self.history: List[HistoricalEvent] = []  # Important historical events
        self.resources: Dict[str, float] = {
            "military": self.military_power,
            "economic": self.economic_power,
            "diplomatic": self.military_power
        }
    
    def update_relationship(self, other_country: str, change: int):
        """Update relationship with another country."""
        current = self.relationships.get(other_country, 0)
        self.relationships[other_country] = max(-100, min(100, current + change))
    
    def get_relationship(self, other_country: str) -> int:
        """Get relationship score with another country."""
        return self.relationships.get(other_country, 0)
    
    def mobilize(self):
        """Mobilize forces."""
        if not self.is_mobilized:
            self.is_mobilized = True
            self.military_power += 10
            self.economic_power -= 5
            self.internal_stability -= 10

    def update_sentiment(self, country_name: str, change: float) -> None:
        """Update sentiment towards another country."""
        current = self.sentiment.get(country_name, 0.0)
        self.sentiment[country_name] = max(-1.0, min(1.0, current + change))
    
    def add_historical_event(self, event: HistoricalEvent) -> None:
        """Add a significant historical event."""
        self.history.append(event)
        
    def get_relationship_context(self, country_name: str) -> Dict[str, Union[RelationType, float, List[HistoricalEvent]]]:
        """Get full context of relationship with another country."""
        return {
            "formal_relation": self.relationships.get(country_name, 0),
            "sentiment": self.sentiment.get(country_name, 0.0),
            "recent_history": [
                event for event in self.history[-5:]  # Last 5 events
                if country_name in event.related_countries
            ]
        }

    def update_internal_stability(self, change: float) -> None:
        """Update the country's internal stability."""
        self.internal_stability = max(0.0, min(100.0, self.internal_stability + change))

    def update_resources(self, resource_type: str, change: float) -> None:
        """Update a specific resource value."""
        if resource_type in self.resources:
            self.resources[resource_type] = max(0.0, self.resources[resource_type] + change) 