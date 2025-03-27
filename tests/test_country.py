import pytest
from src.models.country import Country

def test_country_creation():
    country = Country("TestCountry", 100, "Democratic")
    assert country.name == "TestCountry"
    assert country.strength == 100
    assert country.ideology == "Democratic"
    assert country.state == "Peace"
    assert len(country.relationships) == 0

def test_relationship_setting():
    country1 = Country("Country1", 100, "Democratic")
    country1.set_relationship("Country2", "Ally")
    assert country1.get_relationship("Country2") == "Ally"
    assert country1.get_relationship("NonExistent") == "Neutral"

def test_invalid_relationship():
    country = Country("TestCountry", 100, "Democratic")
    with pytest.raises(ValueError, match="Invalid relationship type"):
        country.set_relationship("OtherCountry", "Invalid")

def test_state_setting():
    country = Country("TestCountry", 100, "Democratic")
    country.set_state("War")
    assert country.state == "War"
    
    with pytest.raises(ValueError, match="Invalid state type"):
        country.set_state("InvalidState") 