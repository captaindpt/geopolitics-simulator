import pytest
from src.models.world import World
from src.models.country import Country
from src.actions.base_action import Action
from src.actions.specific_actions import DeclareWarAction, ProposeAllianceAction, HelpAction
from src.actions.action_factory import ActionFactory

@pytest.fixture
def world():
    world = World()
    
    # Add some test countries
    usa = Country("USA", 90, "Democratic")
    russia = Country("Russia", 85, "Authoritarian")
    china = Country("China", 88, "Authoritarian")
    france = Country("France", 75, "Democratic")
    
    world.add_country(usa)
    world.add_country(russia)
    world.add_country(china)
    world.add_country(france)
    
    return world

def test_declare_war_action(world):
    """Test war declaration execution"""
    action = DeclareWarAction("Declare war on Russia", "USA", "Russia")
    
    assert action.execute(world)
    
    usa = world.get_country("USA")
    russia = world.get_country("Russia")
    
    assert usa.get_relationship("Russia") == "Enemy"
    assert russia.get_relationship("USA") == "Enemy"
    assert usa.state == "War"
    assert russia.state == "War"
    
    # Check event was recorded
    assert any("USA declared war on Russia" in event["text"] for event in world.events)

def test_propose_alliance_same_ideology(world):
    """Test alliance proposal between ideologically aligned countries"""
    action = ProposeAllianceAction("Propose alliance to France", "USA", "France")
    
    assert action.execute(world)
    
    usa = world.get_country("USA")
    france = world.get_country("France")
    
    assert usa.get_relationship("France") == "Ally"
    assert france.get_relationship("USA") == "Ally"
    
    # Check event was recorded
    assert any("USA and France formed an alliance" in event["text"] for event in world.events)

def test_propose_alliance_different_ideology(world):
    """Test alliance proposal between ideologically different countries"""
    action = ProposeAllianceAction("Propose alliance to Russia", "USA", "Russia")
    
    # Should fail without common enemies
    assert not action.execute(world)
    
    usa = world.get_country("USA")
    russia = world.get_country("Russia")
    
    assert usa.get_relationship("Russia") == "Neutral"
    assert russia.get_relationship("USA") == "Neutral"
    
    # Check rejection was recorded
    assert any("Russia rejected USA's alliance proposal" in event["text"] for event in world.events)

def test_propose_alliance_common_enemy(world):
    """Test alliance proposal when countries have a common enemy"""
    # Set up common enemy
    usa = world.get_country("USA")
    russia = world.get_country("Russia")
    france = world.get_country("France")
    
    usa.set_relationship("China", "Enemy")
    france.set_relationship("China", "Enemy")
    
    action = ProposeAllianceAction("Propose alliance to France", "USA", "France")
    
    assert action.execute(world)
    assert usa.get_relationship("France") == "Ally"
    assert france.get_relationship("USA") == "Ally"

def test_help_action(world):
    """Test help action for country at war"""
    # Set up war
    russia = world.get_country("Russia")
    china = world.get_country("China")
    
    russia.set_state("War")
    russia.set_relationship("China", "Enemy")
    china.set_relationship("Russia", "Enemy")
    
    action = HelpAction("Help Russia", "USA", "Russia")
    
    assert action.execute(world)
    
    usa = world.get_country("USA")
    
    assert usa.state == "War"
    assert usa.get_relationship("Russia") == "Ally"
    assert usa.get_relationship("China") == "Enemy"
    assert russia.get_relationship("USA") == "Ally"
    
    # Check event was recorded
    assert any("USA joined Russia's war against China" in event["text"] for event in world.events)

def test_help_action_no_war(world):
    """Test help action when target is not at war"""
    action = HelpAction("Help Russia", "USA", "Russia")
    
    assert not action.execute(world)
    
    usa = world.get_country("USA")
    assert usa.state == "Peace"

def test_action_factory():
    """Test action factory creates correct actions"""
    # Test war declaration
    action = ActionFactory.create_action("Declare war on Russia", "USA")
    assert isinstance(action, DeclareWarAction)
    assert action.source == "USA"
    assert action.target == "Russia"
    
    # Test alliance proposal
    action = ActionFactory.create_action("Propose alliance to France", "USA")
    assert isinstance(action, ProposeAllianceAction)
    assert action.source == "USA"
    assert action.target == "France"
    
    # Test help action
    action = ActionFactory.create_action("Help Russia", "USA")
    assert isinstance(action, HelpAction)
    assert action.source == "USA"
    assert action.target == "Russia"
    
    # Test invalid action
    action = ActionFactory.create_action("Invalid action", "USA")
    assert action is None 