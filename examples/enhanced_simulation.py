import os
from dotenv import load_dotenv
from src.models.world import World
from src.models.country import Country
from src.agents.llm_agent import LLMAgent
from src.simulation.engine import SimulationEngine
from src.visualization.visualizer import WorldVisualizer
from src.config.llm_config import LLMConfig

def setup_world() -> World:
    """Set up a world with multiple countries"""
    world = World()
    
    # Add countries with different ideologies and strengths
    countries = [
        Country("USA", 90, "Democratic"),
        Country("Russia", 85, "Authoritarian"),
        Country("China", 88, "Authoritarian"),
        Country("UK", 82, "Democratic"),
        Country("Iran", 75, "Authoritarian"),
        Country("France", 80, "Democratic"),
        Country("Japan", 78, "Democratic"),
        Country("India", 85, "Democratic")
    ]
    
    for country in countries:
        world.add_country(country)
    
    # Set up initial relationships
    world.set_relationship("USA", "Russia", "Enemy")
    world.set_relationship("USA", "China", "Enemy")
    world.set_relationship("Russia", "China", "Ally")
    world.set_relationship("UK", "USA", "Ally")
    world.set_relationship("Iran", "USA", "Enemy")
    world.set_relationship("France", "UK", "Ally")
    world.set_relationship("Japan", "USA", "Ally")
    world.set_relationship("India", "China", "Tense")
    
    return world

def setup_agents(world: World, api_key: str) -> None:
    """Set up LLM agents for each country"""
    llm_config = LLMConfig(
        max_tokens=200,
        temperature=0.7,
        stream=True
    )
    
    # Create agents with different personalities
    personalities = {
        "USA": "Aggressive",
        "Russia": "Cautious",
        "China": "Neutral",
        "UK": "Cautious",
        "Iran": "Aggressive",
        "France": "Neutral",
        "Japan": "Cautious",
        "India": "Neutral"
    }
    
    for country_name, personality in personalities.items():
        agent = LLMAgent(country_name, personality, api_key, llm_config)
        world.add_agent(agent)

def run_simulation(world: World, num_turns: int = 5) -> None:
    """Run the simulation and visualize results"""
    engine = SimulationEngine(world)
    visualizer = WorldVisualizer(world)
    
    print("\n=== Starting Enhanced Simulation ===")
    print("Initial World State:")
    print(visualizer.generate_text_report())
    
    # Plot initial state
    print("\nPlotting initial relationship network...")
    visualizer.plot_relationship_network()
    
    # Run simulation turns
    for turn in range(num_turns):
        print(f"\n=== Turn {turn + 1} ===")
        
        # Run agent turns
        actions = engine.run_turn()
        
        # Print actions taken
        if actions:
            print("\nActions taken:")
            for action in actions:
                print(f"- {action}")
        
        # Plot current state
        print("\nCurrent World State:")
        print(visualizer.generate_text_report())
        
        # Plot different visualizations
        if turn % 2 == 0:  # Alternate between different visualizations
            print("\nPlotting resource trends for USA...")
            visualizer.plot_resource_trends("USA")
        else:
            print("\nPlotting sentiment network...")
            visualizer.plot_sentiment_network()
    
    # Final visualizations
    print("\n=== Final State ===")
    print(visualizer.generate_text_report())
    print("\nPlotting final relationship network...")
    visualizer.plot_relationship_network()
    print("\nPlotting global trends...")
    visualizer.plot_global_trends()

def main():
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        raise ValueError("HUGGINGFACE_API_KEY not found in environment variables")
    
    # Set up and run simulation
    world = setup_world()
    setup_agents(world, api_key)
    run_simulation(world)

if __name__ == "__main__":
    main() 