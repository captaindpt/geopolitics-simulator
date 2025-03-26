from typing import Dict, List, Optional, Any
from datetime import datetime
from openai import OpenAI
from models.world import World
from models.country import Country, HistoricalEvent
from agents.base_agent import Agent, PersonalityType
from agents.llm_agent import LLMAgent
from actions.action_factory import ActionFactory

class SimulationEngine:
    """Manages the simulation of countries and their interactions."""
    
    def __init__(self):
        self.world = World()
        self.agents: Dict[str, Agent] = {}
        
    def add_country(self, name: str, personality: PersonalityType):
        """Add a country to the simulation."""
        # Create agent
        agent = LLMAgent(name, personality)
        self.agents[name] = agent
        
        # Add country to world
        country = Country(name)
        self.world.add_country(name, country)
        
    def run_simulation(self, num_turns: int = 10):
        """Run the simulation for a specified number of turns."""
        print("\nInitializing World War I simulation (1914)...\n")
        
        for turn in range(1, num_turns + 1):
            print(f"Turn {turn}:")
            
            # Each country makes a decision
            for name, agent in self.agents.items():
                # Get decision
                action = agent.decide(self.world)
                
                # Execute action if any
                if action:
                    action.execute(self.world)
                    print(f"{name} decides to: {action.get_description()}")
                else:
                    print(f"{name} decides to: Do nothing because the situation requires careful observation")
                    
            # Print world state
            self._print_world_state()
            print()
            
    def _print_world_state(self):
        """Print the current state of the world."""
        print("\nWorld State:")
        print(f"Global Tension: {self.world.global_tension:.2f}")
        print(f"Active Conflicts: {list(self.world.active_conflicts)}")
        print("\nRecent Events:")
        for event in self.world.events[-5:]:
            print(f"- {event}")

    def _calculate_action_impact(self, action) -> float:
        """Calculate the impact of an action on global tension."""
        if "Declare war" in action.description:
            return 0.3  # War declarations significantly increase tension
        elif "Propose alliance" in action.description:
            return -0.1  # Alliances slightly decrease tension
        elif "Help" in action.description:
            return 0.1  # Help actions have moderate impact
        return 0.0

    def _get_affected_countries(self, action) -> List[str]:
        """Get list of countries affected by an action."""
        affected = [action.source]
        if action.target:
            affected.append(action.target)
        return affected

    def _resolve_wars(self) -> List[str]:
        """Resolve ongoing wars and return list of events that occurred."""
        events = []
        
        # Find all active wars
        wars = set()
        for name, country in self.world.countries.items():
            if country.state == "War":
                enemies = [enemy for enemy, rel in country.relationships.items() 
                         if rel == "Enemy"]
                for enemy in enemies:
                    wars.add(tuple(sorted([name, enemy])))
        
        # Resolve each war
        for country1, country2 in wars:
            if country1 not in self.world.countries or country2 not in self.world.countries:
                continue
                
            c1 = self.world.countries[country1]
            c2 = self.world.countries[country2]
            
            # Calculate effective strength (including allies)
            c1_strength = self._calculate_effective_strength(c1)
            c2_strength = self._calculate_effective_strength(c2)
            
            # Simple war resolution based on strength ratio
            import random
            if random.random() < 0.1:  # 10% chance of war ending each turn
                if c1_strength > c2_strength * 1.5:
                    events.extend(self._handle_war_victory(c1, c2))
                elif c2_strength > c1_strength * 1.5:
                    events.extend(self._handle_war_victory(c2, c1))
        
        return events

    def _calculate_effective_strength(self, country: Country) -> float:
        """Calculate country's effective strength including allies and internal factors."""
        base_strength = country.strength * country.internal_stability
        
        # Add ally contributions
        ally_strength = sum(
            self.world.countries[ally].strength * 0.5
            for ally, relation in country.relationships.items()
            if relation == "Ally" and ally in self.world.countries
        )
        
        # Factor in resources
        military_factor = country.resources["military"] / country.strength
        economic_factor = country.resources["economic"] / country.strength
        
        return base_strength + ally_strength * (military_factor + economic_factor) / 2

    def _handle_war_victory(self, winner: Country, loser: Country) -> List[str]:
        """Handle the aftermath of a war victory with enhanced state tracking."""
        events = []
        
        # Create victory event
        victory_event = f"{winner.name} has defeated {loser.name} in war"
        events.append(victory_event)
        
        # Update sentiments and stability
        winner.update_sentiment(loser.name, -0.3)
        loser.update_sentiment(winner.name, -0.5)
        loser.update_internal_stability(-0.3)
        
        # Update resources
        winner.update_resources("military", -0.2 * winner.resources["military"])  # War depletes resources
        loser.update_resources("military", -0.4 * loser.resources["military"])
        loser.update_resources("economic", -0.3 * loser.resources["economic"])
        
        # Reset states
        winner.set_state("Peace")
        
        # Check for annexation
        if winner.strength > loser.strength * 3:
            annexation_event = f"{loser.name} has been annexed by {winner.name}"
            self.world.add_event(
                annexation_event,
                impact=0.5,
                affected_countries=[winner.name, loser.name]
            )
            self.world.remove_country(loser.name)
            events.append(annexation_event)
        else:
            loser.set_state("Peace")
            # Reset relationship to neutral but maintain negative sentiment
            winner.set_relationship(loser.name, "Neutral")
            loser.set_relationship(winner.name, "Neutral")
        
        return events

    def run_turn(self) -> List[str]:
        """Run a single turn of the simulation with enhanced state tracking."""
        self.world.turn += 1
        turn_events = []
        
        # Each agent perceives and decides
        for name, agent in self.agents.items():
            if name in self.world.countries:  # Check country still exists
                # Get agent's decision
                action = agent.decide(self.world)
                
                # Execute action if any
                if action:
                    success = action.execute(self.world)
                    if success:
                        # Add event with impact and affected countries
                        self.world.add_event(
                            action.description,
                            impact=self._calculate_action_impact(action),
                            affected_countries=self._get_affected_countries(action)
                        )
                        turn_events.append(action.description)
        
        # Handle war resolution
        war_events = self._resolve_wars()
        turn_events.extend(war_events)
        
        return turn_events 