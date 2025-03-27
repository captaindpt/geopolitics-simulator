from src.models.world import World
from src.models.country import Country
from src.agents.base_agent import Agent

def run_basic_simulation():
    # Create world
    world = World()
    
    # Create some countries
    usa = Country("USA", 90, "Democratic")
    russia = Country("Russia", 85, "Authoritarian")
    china = Country("China", 88, "Authoritarian")
    iran = Country("Iran", 40, "Authoritarian")  # Add a weaker country
    
    # Add countries to world
    world.add_country(usa)
    world.add_country(russia)
    world.add_country(china)
    world.add_country(iran)
    
    # Create and add agents
    usa_agent = Agent("USA", "Aggressive")  # USA is aggressive
    russia_agent = Agent("Russia", "Cautious")  # Russia is cautious
    china_agent = Agent("China", "Neutral")  # China is neutral
    iran_agent = Agent("Iran", "Cautious")  # Iran is cautious
    
    world.add_agent(usa_agent)
    world.add_agent(russia_agent)
    world.add_agent(china_agent)
    world.add_agent(iran_agent)
    
    # Set some initial relationships
    usa.set_relationship("Russia", "Enemy")
    russia.set_relationship("USA", "Enemy")
    
    china.set_relationship("Russia", "Ally")
    russia.set_relationship("China", "Ally")
    
    # Add initial events
    world.add_event("Simulation started with USA, Russia, China, and Iran")
    world.add_event("USA and Russia have tense relations")
    world.add_event("China and Russia form an alliance")
    
    # Run simulation for several turns
    for turn in range(5):
        print(f"\nTurn {turn + 1}:")
        print("-" * 50)
        
        # Get perceptions
        print("Perceptions:")
        for country_name, agent in world.agents.items():
            perception = agent.perceive(world)
            print(f"\n{country_name} perceives:")
            print(perception)
        
        # Get and execute decisions
        print("\nActions:")
        decisions = world.run_agent_turns()
        if decisions:
            for decision in decisions:
                print(f"- {decision}")
        else:
            print("- No actions taken this turn")
        
        # Advance turn
        world.advance_turn()
    
    return world

if __name__ == "__main__":
    world = run_basic_simulation()
    print(f"\nFinal World State:")
    print(f"World contains {len(world.countries)} countries")
    print(f"Current turn: {world.turn}")
    print("\nEvents:")
    for event in world.events:
        print(f"Turn {event['turn']}: {event['text']}")
    
    print("\nCountry States:")
    for country_name, country in world.countries.items():
        print(f"{country_name}: {country.ideology} ({country.state})")
        print("Relationships:")
        for other, relation in country.relationships.items():
            print(f"  - {other}: {relation}")
        print() 