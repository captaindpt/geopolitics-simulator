import pytest
from unittest.mock import Mock, patch
from src.agents.llm_agent import LLMAgent
from src.models.world import World
from src.models.country import Country
from src.config.llm_config import LLMConfig

@pytest.fixture
def world():
    world = World()
    world.add_country(Country("USA", 90, "Democratic"))
    world.add_country(Country("Russia", 85, "Authoritarian"))
    return world

@pytest.fixture
def llm_agent():
    return LLMAgent("USA", "Aggressive", "test_key")

def test_llm_agent_initialization(llm_agent):
    assert llm_agent.country_name == "USA"
    assert llm_agent.personality == "Aggressive"
    assert llm_agent.api_key == "test_key"
    assert isinstance(llm_agent.config, LLMConfig)
    assert llm_agent.headers == {
        "Authorization": "Bearer test_key",
        "Content-Type": "application/json"
    }

@patch('requests.post')
def test_llm_decision_making(mock_post, llm_agent, world):
    # Mock successful API response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "choices": [{"message": {"content": "Declare war on Russia"}}]
    }
    mock_post.return_value = mock_response
    
    decision = llm_agent.decide(world)
    assert decision == "Declare war on Russia"
    
    # Verify API call
    mock_post.assert_called_once()
    args, kwargs = mock_post.call_args
    assert kwargs["headers"] == llm_agent.headers
    assert "messages" in kwargs["json"]

def test_decision_validation(llm_agent):
    # Test invalid decision
    assert llm_agent._validate_decision("Invalid action") == "Do nothing"
    
    # Test valid decisions
    assert llm_agent._validate_decision("Declare war on Russia") == "Declare war on Russia"
    assert llm_agent._validate_decision("Propose alliance to UK") == "Propose alliance to UK"
    assert llm_agent._validate_decision("Help China") == "Help China"
    assert llm_agent._validate_decision("Mobilize forces") == "Mobilize forces"
    assert llm_agent._validate_decision("Sue for peace with Russia") == "Sue for peace with Russia"
    assert llm_agent._validate_decision("Do nothing") == "Do nothing"

@patch('requests.post')
def test_llm_error_handling(mock_post, llm_agent, world):
    # Test API error
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"
    mock_post.return_value = mock_response
    
    decision = llm_agent.decide(world)
    assert decision == "Do nothing"
    
    # Test exception
    mock_post.side_effect = Exception("Connection error")
    decision = llm_agent.decide(world)
    assert decision == "Do nothing" 