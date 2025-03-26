from simulation.engine import SimulationEngine
from agents.base_agent import PersonalityType

def main():
    # Create simulation engine
    engine = SimulationEngine()
    
    # Add countries with their historical personalities
    engine.add_country("GERMANY", PersonalityType.AGGRESSIVE)
    engine.add_country("AUSTRIA", PersonalityType.AGGRESSIVE)
    engine.add_country("RUSSIA", PersonalityType.DIPLOMATIC)
    engine.add_country("FRANCE", PersonalityType.CAUTIOUS)
    engine.add_country("BRITAIN", PersonalityType.DIPLOMATIC)
    engine.add_country("ITALY", PersonalityType.OPPORTUNISTIC)
    engine.add_country("SERBIA", PersonalityType.CAUTIOUS)
    
    # Run simulation
    engine.run_simulation(num_turns=10)

if __name__ == "__main__":
    main() 