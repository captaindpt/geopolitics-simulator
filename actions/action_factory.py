from typing import Optional, Dict, List
from actions.base_action import BaseAction
from actions.declare_war import DeclareWarAction
from actions.mobilize import MobilizeAction
from actions.issue_ultimatum import IssueUltimatumAction
from actions.offer_concessions import OfferConcessionsAction
from actions.request_mediation import RequestMediationAction

class ActionFactory:
    """Factory class for creating actions from decisions."""
    
    # List of valid country names with their historical context
    VALID_COUNTRIES = {
        "GERMANY": "German Empire",
        "AUSTRIA": "Austria-Hungary",
        "FRANCE": "French Republic",
        "RUSSIA": "Russian Empire",
        "UK": "British Empire",
        "SERBIA": "Kingdom of Serbia"
    }
    
    # Pre-existing alliances in 1914
    HISTORICAL_ALLIANCES = {
        "GERMANY": {"AUSTRIA"},
        "AUSTRIA": {"GERMANY"},
        "FRANCE": {"RUSSIA", "UK"},
        "RUSSIA": {"FRANCE", "UK", "SERBIA"},
        "UK": {"FRANCE", "RUSSIA"},
        "SERBIA": {"RUSSIA"}
    }
    
    # Historical rivalries and tensions
    HISTORICAL_TENSIONS = {
        "GERMANY": ["FRANCE", "RUSSIA"],
        "AUSTRIA": ["SERBIA", "RUSSIA"],
        "FRANCE": ["GERMANY"],
        "RUSSIA": ["GERMANY", "AUSTRIA"],
        "SERBIA": ["AUSTRIA"],
        "UK": [],  # UK tried to maintain balance
        "BRITAIN": ["GERMANY"],
        "ITALY": []
    }
    
    def __init__(self):
        self.HISTORICAL_TENSIONS = {
            'AUSTRIA': ['SERBIA', 'RUSSIA'],
            'GERMANY': ['FRANCE', 'RUSSIA'],
            'RUSSIA': ['AUSTRIA', 'GERMANY'],
            'FRANCE': ['GERMANY'],
            'SERBIA': ['AUSTRIA'],
            'BRITAIN': ['GERMANY'],
            'ITALY': []
        }

    def _extract_target_country(self, decision: str) -> Optional[str]:
        """Extract target country from decision string."""
        decision = decision.upper()
        
        # Common keywords that precede country names in decisions
        keywords = ['TO ', 'FROM ', 'WITH ', 'AGAINST ', 'BECAUSE ', 'AND ']
        
        for keyword in keywords:
            if keyword in decision:
                # Get the text after the keyword
                after_keyword = decision.split(keyword)[1]
                # Get the first word (potential country name)
                potential_country = after_keyword.split()[0]
                # Remove any punctuation
                potential_country = potential_country.strip('.,!?')
                # Check if it's a valid country name
                if potential_country in self.HISTORICAL_TENSIONS.keys():
                    return potential_country
                    
        return None

    def create_action(self, country: str, decision: str) -> Optional[BaseAction]:
        """Create an action based on the country's decision."""
        decision = decision.upper()
        
        # Handle "do nothing" explicitly
        if "DO NOTHING" in decision:
            return None
            
        target_country = self._extract_target_country(decision)
        if target_country == country:  # Can't target self
            return None
            
        # Create appropriate action based on decision
        if "DECLARE WAR" in decision and target_country:
            return DeclareWarAction(country, target_country)
            
        if "MOBILIZE" in decision:
            return MobilizeAction(country)
            
        if "ULTIMATUM" in decision and target_country:
            return IssueUltimatumAction(country, target_country)
            
        if "CONCESSIONS" in decision and target_country:
            return OfferConcessionsAction(country, target_country)
            
        if "MEDIATION" in decision and target_country:
            return RequestMediationAction(country, target_country)
            
        return None 