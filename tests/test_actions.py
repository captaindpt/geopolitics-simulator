import pytest
from src.models.world import World
from src.models.country import Country
from src.actions.specific_actions import DeclareWarAction, ProposeAllianceAction, HelpAction
from src.actions.action_factory import ActionFactory

def test_declare_war_action():
    world = World()
    germany = Country("Germany", 80, "Authoritarian")
    france = Country("France", 70, "Democratic")
    world.add_country(germany)
    world.add_country(france)

    action = DeclareWarAction("Germany", "France")
    success = action.execute(world)

    assert success
    assert germany.get_relationship("France") == "Enemy"
    assert france.get_relationship("Germany") == "Enemy"
    assert germany.state == "War"
    assert france.state == "War"
    assert len(world.events) == 1
    assert "Germany declares war on France" in world.events[0]["text"]

def test_propose_alliance_action_accepted():
    world = World()
    germany = Country("Germany", 80, "Authoritarian")
    italy = Country("Italy", 60, "Authoritarian")  # Same ideology
    world.add_country(germany)
    world.add_country(italy)

    action = ProposeAllianceAction("Germany", "Italy")
    success = action.execute(world)

    assert success
    assert germany.get_relationship("Italy") == "Ally"
    assert italy.get_relationship("Germany") == "Ally"
    assert "formed an alliance" in world.events[0]["text"]

def test_propose_alliance_action_rejected():
    world = World()
    germany = Country("Germany", 80, "Authoritarian")
    france = Country("France", 70, "Democratic")  # Different ideology
    world.add_country(germany)
    world.add_country(france)

    action = ProposeAllianceAction("Germany", "France")
    success = action.execute(world)

    assert not success
    assert germany.get_relationship("France") == "Neutral"
    assert france.get_relationship("Germany") == "Neutral"
    assert "rejected" in world.events[0]["text"]

def test_help_action():
    world = World()
    usa = Country("USA", 100, "Democratic")
    uk = Country("UK", 80, "Democratic")
    germany = Country("Germany", 90, "Authoritarian")
    
    # Setup initial state
    world.add_country(usa)
    world.add_country(uk)
    world.add_country(germany)
    
    # UK is at war with Germany
    uk.set_relationship("Germany", "Enemy")
    germany.set_relationship("UK", "Enemy")
    uk.set_state("War")
    germany.set_state("War")

    action = HelpAction("USA", "UK")
    success = action.execute(world)

    assert success
    assert usa.get_relationship("UK") == "Ally"
    assert uk.get_relationship("USA") == "Ally"
    assert usa.get_relationship("Germany") == "Enemy"
    assert germany.get_relationship("USA") == "Enemy"
    assert usa.state == "War"
    assert "joined" in world.events[0]["text"]

def test_action_factory():
    # Test DeclareWar creation
    action = ActionFactory.create_action("Declare war on France", "Germany")
    assert isinstance(action, DeclareWarAction)
    assert action.source_country == "Germany"
    assert action.target_country == "France"

    # Test ProposeAlliance creation
    action = ActionFactory.create_action("Propose alliance to Italy", "Germany")
    assert isinstance(action, ProposeAllianceAction)
    assert action.source_country == "Germany"
    assert action.target_country == "Italy"

    # Test Help creation
    action = ActionFactory.create_action("Help UK", "USA")
    assert isinstance(action, HelpAction)
    assert action.source_country == "USA"
    assert action.target_country == "UK"

    # Test Do nothing
    action = ActionFactory.create_action("Do nothing", "Germany")
    assert action is None 