from simulation.engine import SimulationEngine
import os

def print_turn_summary(snapshot):
    """Print a formatted summary of a turn."""
    print(f"\n{'='*80}")
    print(f"Turn {snapshot['turn']}:")
    print('='*80)
    
    if snapshot['events']:
        print("\nEvents:")
        for event in snapshot['events']:
            print(f"- {event}")
    
    print("\nCountries:")
    for country_data in snapshot['countries'].values():
        # Basic status
        status = f"- {country_data['name']} ({country_data['ideology']})"
        
        # Add state with color
        state = country_data['state']
        if state == "War":
            status += " [AT WAR]"
        elif state == "Peace":
            status += " [PEACE]"
        
        # Add relationships
        relationships = []
        for other, relation in country_data['relationships'].items():
            if relation == "Ally":
                relationships.append(f"Allied with {other}")
            elif relation == "Enemy":
                relationships.append(f"At war with {other}")
        
        if relationships:
            status += f"\n  Relations: {', '.join(relationships)}"
            
        print(status)
    print("-" * 80)

def main():
    # Configure LLM
    llm_config = {
        "base_url": "https://vmjps1ofbtvn2w43.us-east-1.aws.endpoints.huggingface.cloud/v1/",
        "api_key": os.getenv("HUGGINGFACE_API_KEY")
    }

    # Create simulation
    sim = SimulationEngine(llm_config)

    # Add countries with different personalities and ideologies
    sim.add_country_with_agent("USA", 90, "Democratic", "Cautious")
    sim.add_country_with_agent("USSR", 85, "Communist", "Aggressive")
    sim.add_country_with_agent("UK", 70, "Democratic", "Neutral")
    sim.add_country_with_agent("France", 65, "Democratic", "Cautious")
    sim.add_country_with_agent("Germany", 75, "Fascist", "Aggressive")

    print("\nStarting Cold War simulation...")
    print("Initial setup:")
    
    # Run simulation for 10 turns
    history = sim.run_simulation(turns=10)

    # Print results
    for snapshot in history:
        print_turn_summary(snapshot)

if __name__ == "__main__":
    main() 