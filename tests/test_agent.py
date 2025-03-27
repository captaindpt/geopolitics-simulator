import pytest
from src.agents.base_agent import Agent
from src.models.world import World
from src.models.country import Country

@pytest.fixture
def world():
    world = World()
    
    # Add some test countries
    usa = Country("USA", 90, "Democratic")
    russia = Country("Russia", 85, "Authoritarian")
    china = Country("China", 88, "Authoritarian")
    
    world.add_country(usa)
    world.add_country(russia)
    world.add_country(china)
    
    return world

@pytest.fixture
def agent(world):
    return Agent("USA", "Aggressive")

def test_agent_initialization():
    """Test agent creation with valid and invalid parameters"""
    # Valid initialization
    agent = Agent("TestCountry", "Aggressive")
    assert agent.country_name == "TestCountry"
    assert agent.personality == "Aggressive"
    
    # Invalid personality
    with pytest.raises(ValueError):
        Agent("TestCountry", "Invalid")

def test_agent_perception(world, agent):
    """Test agent's perception generation"""
    # Add some events
    world.add_event("Test event 1")
    world.add_event("Test event 2")
    
    # Set some relationships
    usa = world.get_country("USA")
    usa.set_relationship("Russia", "Enemy")
    
    perception = agent.perceive(world)
    
    # Check perception contains key elements
    assert "USA" in perception
    assert "Democratic" in perception
    assert "Russia" in perception
    assert "Enemy" in perception
    assert "Test event" in perception

def test_agent_memory(world, agent):
    """Test agent's memory management"""
    # Add multiple events
    for i in range(12):  # More than memory limit
        world.add_event(f"Event {i}")
        agent.perceive(world)
    
    # Check memory limit
    assert len(agent.memory) == 10
    assert "Event 11" in agent.memory[-1]

def test_aggressive_agent_decisions(world, agent):
    """Test aggressive agent's decision making"""
    usa = world.get_country("USA")
    weak_country = Country("WeakCountry", 30, "Democratic")
    world.add_country(weak_country)
    
    decision = agent.decide(world)
    assert "Declare war on WeakCountry" in decision

def test_cautious_agent_decisions(world):
    """Test cautious agent's decision making"""
    cautious_agent = Agent("USA", "Cautious")
    usa = world.get_country("USA")
    usa.set_state("Peace")
    
    # Add a war nearby
    russia = world.get_country("Russia")
    russia.set_state("War")
    
    decision = cautious_agent.decide(world)
    assert decision == "Do nothing"

def test_wartime_decisions(world, agent):
    """Test agent decisions during wartime"""
    usa = world.get_country("USA")
    usa.set_state("War")
    usa.set_relationship("Russia", "Enemy")
    
    decision = agent.decide(world)
    assert "Propose alliance" in decision or "Do nothing" in decision 