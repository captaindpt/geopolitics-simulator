from simulation.engine import SimulationEngine
from datetime import datetime
import os

def print_enhanced_turn_summary(snapshot):
    """Print a detailed formatted summary of a turn with enhanced state information."""
    print(f"\n{'='*100}")
    print(f"Turn {snapshot['turn']}:")
    print('='*100)
    
    # Print global state
    global_state = snapshot['global_state']
    print("\nGlobal State:")
    print(f"- Global Tension: {global_state['global_tension']:.2f}")
    print(f"- Active Conflicts: {global_state['active_conflicts']}")
    print(f"- Major Alliances: {global_state['major_alliances']}")
    
    # Print events
    if snapshot['events']:
        print("\nEvents:")
        for event in snapshot['events']:
            print(f"- {event}")
    
    # Print detailed country information
    print("\nCountries:")
    for country_data in snapshot['countries'].values():
        # Basic status
        print(f"\n{country_data['name']} ({country_data['ideology']}):")
        print(f"  State: {country_data['state']}")
        print(f"  Internal Stability: {country_data['internal_stability']:.2f}")
        
        # Resources
        print("  Resources:")
        for resource, value in country_data['resources'].items():
            print(f"    - {resource}: {value:.1f}")
        
        # Relationships and Sentiments
        if country_data['relationships'] or country_data['sentiment']:
            print("  Diplomatic Status:")
            for other_country, relation in country_data['relationships'].items():
                sentiment = country_data['sentiment'].get(other_country, 0.0)
                print(f"    - {other_country}: {relation} (Sentiment: {sentiment:.2f})")
    
    print("-" * 100)

def main():
    # Configure LLM
    llm_config = {
        "base_url": "https://vmjps1ofbtvn2w43.us-east-1.aws.endpoints.huggingface.cloud/v1/",
        "api_key": os.getenv("HUGGINGFACE_API_KEY")
    }

    # Create simulation with LLM support
    sim = SimulationEngine(llm_config)

    # Add countries with different personalities and ideologies
    print("\nInitializing Cold War simulation with enhanced state tracking...")
    
    # Major Powers
    sim.add_country_with_agent("USA", 100, "Democratic", "Cautious")
    sim.add_country_with_agent("USSR", 95, "Communist", "Aggressive")
    
    # European Powers
    sim.add_country_with_agent("UK", 80, "Democratic", "Cautious")
    sim.add_country_with_agent("France", 75, "Democratic", "Neutral")
    sim.add_country_with_agent("West Germany", 70, "Democratic", "Cautious")
    sim.add_country_with_agent("East Germany", 65, "Communist", "Aggressive")
    
    # Add initial relationships
    world = sim.world
    
    # Western Alliance
    world.add_alliance(
        members=["USA", "UK", "France", "West Germany"],
        strength=0.8,
        type_="Military"
    )
    
    # Eastern Alliance
    world.add_alliance(
        members=["USSR", "East Germany"],
        strength=0.7,
        type_="Military"
    )
    
    # Set initial relationships
    for western in ["USA", "UK", "France", "West Germany"]:
        for other_western in ["USA", "UK", "France", "West Germany"]:
            if western != other_western:
                world.countries[western].set_relationship(other_western, "Ally")
                world.countries[western].update_sentiment(other_western, 0.7)
    
    for eastern in ["USSR", "East Germany"]:
        for other_eastern in ["USSR", "East Germany"]:
            if eastern != other_eastern:
                world.countries[eastern].set_relationship(other_eastern, "Ally")
                world.countries[eastern].update_sentiment(other_eastern, 0.7)
    
    # Add some initial tension
    world.add_event(
        "Berlin Wall construction begins",
        impact=0.4,
        affected_countries=["USA", "USSR", "East Germany", "West Germany"]
    )
    
    print("\nStarting simulation...")
    print("Initial setup:")
    
    # Run simulation for 10 turns
    history = sim.run_simulation(turns=10)

    # Print detailed results
    for snapshot in history:
        print_enhanced_turn_summary(snapshot)

if __name__ == "__main__":
    main() 