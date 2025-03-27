import pytest
from src.models.world import World
from src.models.country import Country

def test_world_creation():
    world = World()
    assert world.turn == 0
    assert len(world.countries) == 0
    assert len(world.events) == 0

def test_adding_country():
    world = World()
    country = Country("TestCountry", 100, "Democratic")
    world.add_country(country)
    assert "TestCountry" in world.countries
    assert world.get_country("TestCountry") == country
    assert world.get_country("NonExistent") is None

def test_adding_event():
    world = World()
    world.add_event("Test event occurred")
    assert len(world.events) == 1
    assert world.events[0]["text"] == "Test event occurred"
    assert world.events[0]["turn"] == 0

def test_advancing_turn():
    world = World()
    world.add_event("First turn")
    world.advance_turn()
    world.add_event("Second turn")
    
    assert world.turn == 1
    assert len(world.events) == 2
    assert world.events[0]["turn"] == 0
    assert world.events[1]["turn"] == 1 