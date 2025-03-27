from src.models.world import World
from src.models.country import Country
from src.agents.base_agent import Agent
from src.simulation.engine import SimulationEngine

def analyze_results(history):
    """Analyze simulation results"""
    print("\n=== Simulation Analysis ===")
    
    # Count wars and alliances
    wars = 0
    alliances = 0
    for snapshot in history:
        for country_data in snapshot["countries"].values():
            if country_data["state"] == "War":
                wars += 1
            for rel in country_data["relationships"].values():
                if rel == "Allied":
                    alliances += 1
    
    print(f"Total wars declared: {wars}")
    print(f"Total alliances formed: {alliances}")
    
    # Analyze country relationships
    print("\nFinal Country Relationships:")
    final_state = history[-1]["countries"]
    for country_name, data in final_state.items():
        print(f"\n{country_name}:")
        print(f"  State: {data['state']}")
        print(f"  Ideology: {data['ideology']}")
        print("  Relationships:")
        for other, rel in data["relationships"].items():
            print(f"    - {other}: {rel}")

def main():
    # Create world
    world = World()
    
    # Add countries with different ideologies and strengths
    countries = [
        Country("USA", 90, "Democratic"),
        Country("Russia", 85, "Authoritarian"),
        Country("China", 88, "Authoritarian"),
        Country("UK", 82, "Democratic"),
        Country("Iran", 75, "Authoritarian")
    ]
    
    for country in countries:
        world.add_country(country)
    
    # Add agents with different behaviors
    agents = [
        Agent("USA", "Aggressive"),
        Agent("Russia", "Cautious"),
        Agent("China", "Neutral"),
        Agent("UK", "Cautious"),
        Agent("Iran", "Aggressive")
    ]
    
    for agent in agents:
        world.add_agent(agent)
    
    # Set up initial relationships
    world.set_relationship("USA", "Russia", "Enemy")
    world.set_relationship("USA", "China", "Enemy")
    world.set_relationship("Russia", "China", "Ally")
    world.set_relationship("UK", "USA", "Ally")
    world.set_relationship("Iran", "USA", "Enemy")
    
    # Create simulation engine
    engine = SimulationEngine(world)
    
    print("Starting Advanced Simulation...")
    print("Initial World State:")
    print(f"Number of countries: {len(world.countries)}")
    print(f"Number of agents: {len(world.agents)}")
    
    # Run simulation for 5 turns
    history = engine.run_simulation(5)
    
    # Analyze results
    analyze_results(history)
    
    print("\nSimulation completed successfully!")

if __name__ == "__main__":
    main() 