import pytest
from src.simulation.engine import SimulationEngine

def test_simulation_initialization():
    """Test basic simulation engine initialization."""
    engine = SimulationEngine()
    assert engine.world is not None
    assert len(engine.agents) == 0
    assert engine.llm_client is None

    # Test with LLM config
    llm_config = {
        "base_url": "test_url",
        "api_key": "test_key"
    }
    engine_with_llm = SimulationEngine(llm_config)
    assert engine_with_llm.llm_client is not None

def test_add_country_with_agent():
    """Test adding a country with its agent."""
    engine = SimulationEngine()
    engine.add_country_with_agent("TestCountry", 100, "Democratic", "Neutral")
    
    assert "TestCountry" in engine.world.countries
    assert "TestCountry" in engine.agents
    
    country = engine.world.countries["TestCountry"]
    assert country.strength == 100
    assert country.ideology == "Democratic"
    assert country.state == "Peace"
    
    agent = engine.agents["TestCountry"]
    assert agent.personality == "Neutral"

def test_run_turn_with_war():
    """Test running a turn with countries at war."""
    engine = SimulationEngine()
    
    # Add two countries
    engine.add_country_with_agent("Strong", 100, "Democratic", "Aggressive")
    engine.add_country_with_agent("Weak", 30, "Authoritarian", "Neutral")
    
    # Set them as enemies
    engine.world.countries["Strong"].set_relationship("Weak", "Enemy")
    engine.world.countries["Weak"].set_relationship("Strong", "Enemy")
    engine.world.countries["Strong"].set_state("War")
    engine.world.countries["Weak"].set_state("War")
    
    # Run a turn
    events = engine.run_turn()
    assert isinstance(events, list)
    assert engine.world.turn == 1

def test_war_resolution():
    """Test war resolution mechanics."""
    engine = SimulationEngine()
    
    # Add two countries with very different strengths
    engine.add_country_with_agent("Strong", 100, "Democratic", "Aggressive")
    engine.add_country_with_agent("Weak", 30, "Authoritarian", "Neutral")
    
    # Set them as enemies at war
    engine.world.countries["Strong"].set_relationship("Weak", "Enemy")
    engine.world.countries["Weak"].set_relationship("Strong", "Enemy")
    engine.world.countries["Strong"].set_state("War")
    engine.world.countries["Weak"].set_state("War")
    
    # Run several turns until war resolves
    war_resolved = False
    for _ in range(20):  # Max 20 turns
        events = engine.run_turn()
        if any("defeated" in event for event in events):
            war_resolved = True
            break
    
    assert war_resolved, "War should have been resolved within 20 turns"
    assert "Strong" in engine.world.countries
    assert engine.world.countries["Strong"].state == "Peace"
    assert "Weak" not in engine.world.countries  # Should be annexed

def test_run_simulation():
    """Test running a full simulation."""
    engine = SimulationEngine()
    
    # Add several countries
    engine.add_country_with_agent("USA", 90, "Democratic", "Cautious")
    engine.add_country_with_agent("USSR", 85, "Communist", "Aggressive")
    engine.add_country_with_agent("UK", 70, "Democratic", "Neutral")
    
    # Run simulation
    history = engine.run_simulation(turns=5)
    
    assert len(history) == 5
    for snapshot in history:
        assert "turn" in snapshot
        assert "events" in snapshot
        assert "countries" in snapshot
        assert isinstance(snapshot["events"], list)
        assert isinstance(snapshot["countries"], dict) 