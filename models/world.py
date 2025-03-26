from typing import Dict, List, TypedDict, Optional, Set
from datetime import datetime
from .country import Country, HistoricalEvent
from actions.cooldown import ActionCooldown

class Event(TypedDict):
    turn: int
    text: str
    impact: float
    affected_countries: List[str]

class Conflict(TypedDict):
    """Represents an active conflict between countries."""
    participants: List[str]
    start_turn: int
    intensity: float  # 0.0 to 1.0
    type: str  # "War", "Dispute", "Crisis"

class Alliance(TypedDict):
    """Represents a formal alliance between countries."""
    members: List[str]
    formed_turn: int
    strength: float  # 0.0 to 1.0
    type: str  # "Military", "Economic", "Diplomatic"

class World:
    """
    Represents the simulation world with enhanced global state tracking.
    """
    def __init__(self):
        self.countries: Dict[str, Country] = {}
        self.turn: int = 0
        self.events: List[str] = []
        
        # Enhanced global state tracking
        self.global_tension: float = 0.5  # Start at moderate tension
        self.active_conflicts: Set[str] = set()
        self.alliances: Dict[str, Set[str]] = {
            'AUSTRIA': {'GERMANY', 'ITALY'},
            'GERMANY': {'AUSTRIA', 'ITALY'},
            'RUSSIA': {'FRANCE', 'BRITAIN'},
            'FRANCE': {'RUSSIA', 'BRITAIN'},
            'BRITAIN': {'FRANCE', 'RUSSIA'},
            'ITALY': {'AUSTRIA', 'GERMANY'},
            'SERBIA': set()
        }
        self.cooldown_manager = ActionCooldown()
        
        # Initialize with historical alliances
        self._add_initial_events()
    
    def _add_initial_events(self):
        """Add initial historical events."""
        self.add_event("Alliance formed between FRANCE and BRITAIN")
        self.add_event("Alliance formed between RUSSIA and BRITAIN")
        self.add_event("Archduke Franz Ferdinand assassinated in Sarajevo")
    
    def add_country(self, name: str, country: Country) -> None:
        """Add a country to the world."""
        self.countries[name] = country
    
    def remove_country(self, country_name: str) -> None:
        """Remove a country from the world."""
        if country_name in self.countries:
            del self.countries[country_name]
    
    def add_event(self, event: str):
        """Add an event and update global tension."""
        self.events.append(event)
        if len(self.events) > 5:  # Keep only recent events
            self.events.pop(0)
            
        # Update global tension based on event type
        tension_changes = {
            'DECLARE WAR': 0.2,
            'MOBILIZE': 0.1,
            'ULTIMATUM': 0.15,
            'ALLIANCE': -0.05,
            'CONCESSIONS': -0.1,
            'MEDIATION': -0.05
        }
        
        event_upper = event.upper()
        for event_type, change in tension_changes.items():
            if event_type in event_upper:
                self.global_tension = min(1.0, max(0.0, self.global_tension + change))
                break
        
        # Create historical event for affected countries
        affected_countries = [country for country, c in self.countries.items() if country in event]
        if affected_countries:
            hist_event = HistoricalEvent(
                timestamp=datetime.now(),
                description=event,
                impact=self.global_tension,
                related_countries=affected_countries
            )
            for country_name in affected_countries:
                if country_name in self.countries:
                    self.countries[country_name].add_historical_event(hist_event)
        
        # Update affected countries' internal stability
        for country_name in affected_countries:
            if country_name in self.countries:
                country = self.countries[country_name]
                country.internal_stability = max(0.0, country.internal_stability - self.global_tension * 0.1)
    
    def get_country(self, country_name: str) -> Country:
        """Get a country by name."""
        return self.countries[country_name]
    
    def add_conflict(self, conflict: str):
        """Add a conflict and increase global tension."""
        self.active_conflicts.add(conflict)
        self.global_tension = min(1.0, self.global_tension + 0.2)
        
    def remove_conflict(self, conflict: str):
        """Remove a conflict and decrease global tension."""
        if conflict in self.active_conflicts:
            self.active_conflicts.remove(conflict)
            self.global_tension = max(0.0, self.global_tension - 0.1)
        
    def get_allies(self, country: str) -> Set[str]:
        """Get allies of a country."""
        return self.alliances.get(country, set())
        
    def get_enemies(self, country: str) -> Set[str]:
        """Get countries currently in conflict with the given country."""
        enemies = set()
        for conflict in self.active_conflicts:
            countries = conflict.split('-')
            if country in countries:
                enemies.update(c for c in countries if c != country)
        return enemies
    
    def get_world_state_summary(self) -> Dict:
        """Get a semantic summary of current world state."""
        return {
            "turn": self.turn,
            "global_tension": self.global_tension,
            "active_conflicts": len(self.active_conflicts),
            "major_alliances": len(self.alliances),
            "recent_events": self.events[-5:] if self.events else []
        }

    def update_relationship(self, source: str, target: str, change: int):
        """Update the relationship between two countries."""
        if source in self.countries and target in self.countries:
            self.countries[source].update_relationship(target, change)
            self.countries[target].update_relationship(source, change)
            
    def add_alliance(self, members: List[str]):
        """Add an alliance between multiple countries."""
        for i in range(len(members)):
            for j in range(i + 1, len(members)):
                self.update_relationship(members[i], members[j], 30)
                self.add_event(f"Alliance formed between {members[i]} and {members[j]}")
                
    def get_country_allies(self, country: str) -> List[str]:
        """Get a list of allies for a country."""
        if country not in self.countries:
            return []
        return [name for name, c in self.countries.items() 
                if c.get_relationship(country) >= 50 and name != country]
                
    def get_country_enemies(self, country: str) -> List[str]:
        """Get a list of enemies for a country."""
        if country not in self.countries:
            return []
        return [name for name, c in self.countries.items() 
                if c.get_relationship(country) <= -50 and name != country] 