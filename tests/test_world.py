import pytest
from src.models.world import World
from src.models.country import Country

def test_world_initialization():
    world = World()
    assert world.turn == 0
    assert len(world.countries) == 0
    assert len(world.events) == 0

def test_country_management():
    world = World()
    country = Country("TestCountry", 100, "Democratic")
    
    world.add_country(country)
    assert "TestCountry" in world.countries
    
    world.remove_country("TestCountry")
    assert "TestCountry" not in world.countries

def test_event_recording():
    world = World()
    world.add_event("Test event occurred")
    assert len(world.events) == 1
    assert world.events[0]["text"] == "Test event occurred"
    assert world.events[0]["turn"] == 0 