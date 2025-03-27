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
    
    # Set up WWI scenario with historical context
    sim.add_country("Germany", {
        "ideology": "Imperial",
        "personality": "Aggressive",
        "strength": 85,
        "allies": ["Austria-Hungary"],
        "enemies": ["France", "Russia"],
        "historical_context": "A rapidly industrializing power seeking its place in the sun, with growing military might and colonial ambitions."
    })
    
    sim.add_country("Austria-Hungary", {
        "ideology": "Imperial",
        "personality": "Aggressive",
        "strength": 70,
        "allies": ["Germany"],
        "enemies": ["Serbia"],
        "historical_context": "A multi-ethnic empire facing internal tensions and nationalist movements, particularly in the Balkans."
    })
    
    sim.add_country("Russia", {
        "ideology": "Imperial",
        "personality": "Aggressive",
        "strength": 75,
        "allies": ["France", "Britain"],
        "enemies": ["Germany", "Austria-Hungary"],
        "historical_context": "The largest European power, with pan-Slavic ambitions and a desire to protect its influence in the Balkans."
    })
    
    sim.add_country("France", {
        "ideology": "Democratic",
        "personality": "Neutral",
        "strength": 80,
        "allies": ["Britain", "Russia"],
        "enemies": ["Germany"],
        "historical_context": "A republic still smarting from its defeat in the Franco-Prussian War, seeking to maintain its colonial empire."
    })
    
    sim.add_country("Britain", {
        "ideology": "Democratic",
        "personality": "Cautious",
        "strength": 90,
        "allies": ["France", "Russia"],
        "enemies": ["Germany"],
        "historical_context": "The world's leading naval power, concerned about maintaining the balance of power in Europe."
    })
    
    sim.add_country("Serbia", {
        "ideology": "Nationalist",
        "personality": "Aggressive",
        "strength": 30,
        "allies": ["Russia"],
        "enemies": ["Austria-Hungary"],
        "historical_context": "A small but fiercely independent nation, the center of pan-Slavic nationalism in the Balkans."
    })
    
    # Add initial events with rich narratives
    sim.add_event({
        "text": "Archduke Franz Ferdinand was assassinated in Sarajevo",
        "narrative": "In a shocking turn of events that would change the course of history, Archduke Franz Ferdinand, heir to the Austro-Hungarian throne, was assassinated in Sarajevo by a Serbian nationalist. The streets of the Bosnian capital erupted in chaos as the news spread, while the world held its breath, knowing this could be the spark that ignites a powder keg of European tensions.",
        "impact": {
            "Austria-Hungary": -0.3,
            "Serbia": -0.2,
            "global": -0.1
        },
        "category": "Political"
    })
    
    sim.add_event({
        "text": "Austria-Hungary issued an ultimatum to Serbia",
        "narrative": "The Austro-Hungarian Empire, reeling from the assassination of its heir, delivered a harsh ultimatum to Serbia. The demands were intentionally designed to be unacceptable, as Vienna sought a pretext for military action. The international community watched anxiously as the clock ticked down on Serbia's response.",
        "impact": {
            "Austria-Hungary": -0.1,
            "Serbia": -0.2,
            "global": -0.1
        },
        "category": "Diplomatic"
    })
    
    sim.add_event({
        "text": "Serbia partially accepted Austria-Hungary's ultimatum",
        "narrative": "In a carefully crafted response, Serbia accepted most of Austria-Hungary's demands but rejected those that would compromise its sovereignty. This partial acceptance, while demonstrating a willingness to cooperate, was not enough to satisfy Vienna. The diplomatic crisis deepened as both sides prepared for the worst.",
        "impact": {
            "Austria-Hungary": -0.2,
            "Serbia": -0.1,
            "global": -0.1
        },
        "category": "Diplomatic"
    })
    
    # Run simulation
    print("Starting WWI simulation...")
    history = sim.run(turns=10)
    
    # Analyze results with narrative focus
    print("\nSimulation Results:")
    for turn in history:
        print(f"\nTurn {turn['turn']}:")
        print(f"\n{turn['narrative']}")
        
        print("\nKey Events:")
        for event in turn['events']:
            print(f"- {event.get('narrative', event['text'])}")
            
        print("\nWorld State:")
        for country, state in turn['countries'].items():
            print(f"\n{state['narrative']}")

if __name__ == "__main__":
    main() 