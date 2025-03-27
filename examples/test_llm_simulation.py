import os
from dotenv import load_dotenv
from src.models.world import World
from src.models.country import Country
from src.agents.llm_agent import LLMAgent
from src.config.llm_config import LLMConfig

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv("HUGGINGFACE_API_KEY")
    if not api_key:
        raise ValueError("HUGGINGFACE_API_KEY not found in environment variables or .env file")

    # Create a simple world with two countries
    world = World()
    usa = Country("USA", 90, "Democratic")
    russia = Country("Russia", 85, "Authoritarian")
    
    world.add_country(usa)
    world.add_country(russia)
    
    # Set initial relationship
    world.set_relationship("USA", "Russia", "Enemy")
    
    # Create LLM config
    config = LLMConfig(
        model="tgi",
        max_tokens=150,
        temperature=0.7,
        stream=False  # Disable streaming for simpler testing
    )
    
    # Create LLM agent
    agent = LLMAgent("USA", "Aggressive", api_key, config)
    
    print("\nInitial World State:")
    print(f"USA (Democratic, Strength: {usa.strength})")
    print(f"Russia (Authoritarian, Strength: {russia.strength})")
    print(f"Relationship: {usa.get_relationship('Russia')}")
    
    print("\nGetting agent's perception...")
    perception = agent.perceive(world)
    print(perception)
    
    print("\nGetting agent's decision...")
    decision = agent.decide(world)
    print(f"Decision: {decision}")

if __name__ == "__main__":
    main() 