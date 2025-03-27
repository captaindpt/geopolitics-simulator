import os
from dotenv import load_dotenv
from src.simulation import Simulation
from src.llm import LLMClient

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize LLM client
    llm = LLMClient(
        base_url="https://vmjps1ofbtvn2w43.us-east-1.aws.endpoints.huggingface.cloud/v1/",
        api_key=os.getenv("HUGGINGFACE_API_KEY")
    )
    
    # Create simulation
    sim = Simulation(llm)
    
    # Set up WWI scenario
    sim.add_country("Germany", {
        "ideology": "Imperial",
        "personality": "Aggressive",
        "strength": 85,
        "allies": ["Austria-Hungary"],
        "enemies": ["France", "Russia"]
    })
    
    sim.add_country("Austria-Hungary", {
        "ideology": "Imperial",
        "personality": "Aggressive",
        "strength": 70,
        "allies": ["Germany"],
        "enemies": ["Serbia"]
    })
    
    sim.add_country("Russia", {
        "ideology": "Imperial",
        "personality": "Aggressive",
        "strength": 75,
        "allies": ["France", "Britain"],
        "enemies": ["Germany", "Austria-Hungary"]
    })
    
    sim.add_country("France", {
        "ideology": "Democratic",
        "personality": "Neutral",
        "strength": 80,
        "allies": ["Britain", "Russia"],
        "enemies": ["Germany"]
    })
    
    sim.add_country("Britain", {
        "ideology": "Democratic",
        "personality": "Cautious",
        "strength": 90,
        "allies": ["France", "Russia"],
        "enemies": ["Germany"]
    })
    
    sim.add_country("Serbia", {
        "ideology": "Nationalist",
        "personality": "Aggressive",
        "strength": 30,
        "allies": ["Russia"],
        "enemies": ["Austria-Hungary"]
    })
    
    # Add initial events
    sim.add_event({
        "text": "Archduke Franz Ferdinand was assassinated in Sarajevo by a Serbian nationalist",
        "impact": {
            "Austria-Hungary": -0.3,
            "Serbia": -0.2,
            "global": -0.1
        }
    })
    
    sim.add_event({
        "text": "Austria-Hungary issued an ultimatum to Serbia with harsh demands",
        "impact": {
            "Austria-Hungary": -0.1,
            "Serbia": -0.2,
            "global": -0.1
        }
    })
    
    sim.add_event({
        "text": "Serbia partially accepted Austria-Hungary's ultimatum but rejected some demands",
        "impact": {
            "Austria-Hungary": -0.2,
            "Serbia": -0.1,
            "global": -0.1
        }
    })
    
    # Run simulation
    print("Starting WWI simulation...")
    history = sim.run(turns=10)
    
    # Analyze results
    print("\nSimulation Results:")
    for turn in history:
        print(f"\nTurn {turn['turn']}:")
        for event in turn['events']:
            print(f"- {event['text']}")
        print("\nWorld State:")
        for country, state in turn['countries'].items():
            print(f"{country}: {state['state']}")

if __name__ == "__main__":
    main() 