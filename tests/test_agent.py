import pytest
from src.agents.base_agent import Agent
from src.models.world import World
from src.models.country import Country

@pytest.fixture
def test_world():
    world = World()
    
    # Add some test countries
    germany = Country("Germany", 85, "Authoritarian")
    britain = Country("Britain", 90, "Democratic")
    france = Country("France", 80, "Democratic")
    
    world.add_country(germany)
    world.add_country(britain)
    world.add_country(france)
    
    return world

def test_agent_creation():
    agent = Agent("TestCountry", "Aggressive")
    assert agent.country_name == "TestCountry"
    assert agent.personality == "Aggressive"
    assert len(agent.memory) == 0

def test_agent_perception(test_world):
    agent = Agent("Germany", "Aggressive")
    perception = agent.perceive(test_world)
    
    assert "Germany" in perception
    assert "Authoritarian" in perception
    assert "Peace" in perception

def test_aggressive_agent_decision(test_world):
    agent = Agent("Germany", "Aggressive")
    perception = agent.perceive(test_world)
    decision = agent.decide(test_world, perception)
    
    # Should consider attacking weaker nations
    assert decision.startswith("Declare war on") or decision == "Do nothing"

def test_cautious_agent_decision(test_world):
    agent = Agent("Britain", "Cautious")
    
    # Put Britain at war
    britain = test_world.get_country("Britain")
    britain.set_state("War")
    britain.set_relationship("Germany", "Enemy")
    
    perception = agent.perceive(test_world)
    decision = agent.decide(test_world, perception)
    
    # Should try to find allies when at war
    assert decision.startswith("Propose alliance to") or decision == "Do nothing"

def test_neutral_agent_decision(test_world):
    agent = Agent("France", "Neutral")
    
    # Set up a scenario where an ideologically aligned country is at war
    britain = test_world.get_country("Britain")
    britain.set_state("War")
    
    perception = agent.perceive(test_world)
    decision = agent.decide(test_world, perception)
    
    # Should consider helping ideologically aligned countries
    assert decision.startswith("Help") or decision == "Do nothing"

def test_agent_memory_empty_initially():
    agent = Agent("TestCountry", "Neutral")
    assert len(agent.memory) == 0

def test_perception_with_relationships(test_world):
    # Set up some relationships
    germany = test_world.get_country("Germany")
    germany.set_relationship("Britain", "Enemy")
    germany.set_relationship("France", "Ally")
    
    agent = Agent("Germany", "Aggressive")
    perception = agent.perceive(test_world)
    
    assert "Britain" in perception
    assert "France" in perception
    assert "enemies" in perception.lower()
    assert "allies" in perception.lower()

def test_perception_with_events(test_world):
    # Add some test events
    test_world.add_event("Major conflict breaks out")
    test_world.add_event("Peace treaty signed")
    
    agent = Agent("Germany", "Aggressive")
    perception = agent.perceive(test_world)
    
    assert "Major conflict breaks out" in perception
    assert "Peace treaty signed" in perception 