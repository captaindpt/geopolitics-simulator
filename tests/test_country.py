import pytest
from src.models.country import Country

def test_country_initialization():
    country = Country("TestCountry", 100, "Democratic")
    assert country.name == "TestCountry"
    assert country.strength == 100
    assert country.ideology == "Democratic"
    assert country.state == "Peace"
    assert len(country.relationships) == 0

def test_relationship_management():
    country = Country("TestCountry", 100, "Democratic")
    country.set_relationship("OtherCountry", "Ally")
    assert country.get_relationship("OtherCountry") == "Ally"
    assert country.get_relationship("NonexistentCountry") == "Neutral"

def test_state_changes():
    country = Country("TestCountry", 100, "Democratic")
    country.set_state("War")
    assert country.state == "War" 