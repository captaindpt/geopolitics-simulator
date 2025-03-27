import pytest
from src.models.world import World
from src.models.country import Country
from src.agents.base_agent import Agent
from src.simulation.engine import SimulationEngine

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
    
    # Add agents
    world.add_agent(Agent("USA", "Aggressive"))
    world.add_agent(Agent("Russia", "Cautious"))
    world.add_agent(Agent("China", "Neutral"))
    
    return world

@pytest.fixture
def simulation_engine(world):
    return SimulationEngine(world)

def test_single_turn_execution(simulation_engine):
    """Test running a single turn"""
    actions = simulation_engine.run_turn()
    assert isinstance(actions, list)
    assert len(simulation_engine.history) == 1
    
    # Check snapshot format
    snapshot = simulation_engine.history[0]
    assert "turn" in snapshot
    assert "countries" in snapshot
    assert "events" in snapshot
    
    # Check turn advanced
    assert simulation_engine.world.turn == 2  # Turn is advanced after snapshot

def test_multiple_turns(simulation_engine):
    """Test running multiple turns"""
    history = simulation_engine.run_simulation(3)
    assert len(history) == 3
    assert len(simulation_engine.history) == 3
    
    # Check turn progression
    assert history[0]["turn"] == 1
    assert history[1]["turn"] == 2
    assert history[2]["turn"] == 3
    
    # Check final world state
    assert simulation_engine.world.turn == 4  # Turn is advanced after last snapshot

def test_simulation_stop(simulation_engine):
    """Test stopping simulation"""
    # Run for 5 turns but stop after turn 2
    simulation_engine.run_simulation(2)
    simulation_engine.stop()
    history = simulation_engine.run_simulation(3)
    
    assert len(history) == 0  # Should not run any more turns
    assert simulation_engine.world.turn == 3  # Turn is advanced after last snapshot

def test_world_state_tracking(simulation_engine):
    """Test world state tracking across turns"""
    # Run simulation
    history = simulation_engine.run_simulation(3)
    
    # Check state progression
    for i in range(len(history) - 1):
        current = history[i]
        next_state = history[i + 1]
        
        # Turn should increment
        assert next_state["turn"] == current["turn"] + 1
        
        # Check events accumulation
        assert len(next_state["events"]) >= len(current["events"])
        
        # Check countries remain consistent
        assert set(current["countries"].keys()) == set(next_state["countries"].keys())

def test_snapshot_format(simulation_engine):
    """Test snapshot format and content"""
    simulation_engine.run_turn()
    snapshot = simulation_engine.history[0]
    
    # Check required fields
    assert "turn" in snapshot
    assert "countries" in snapshot
    assert "events" in snapshot
    
    # Check country data format
    for country_data in snapshot["countries"].values():
        assert "name" in country_data
        assert "strength" in country_data
        assert "ideology" in country_data
        assert "state" in country_data
        assert "relationships" in country_data
        
    # Check events format
    for event in snapshot["events"]:
        assert "turn" in event
        assert "text" in event 