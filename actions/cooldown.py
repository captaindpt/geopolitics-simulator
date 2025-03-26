from typing import Dict, Set
from datetime import datetime, timedelta

class ActionCooldown:
    """Manages cooldown periods for different actions in the simulation."""
    
    def __init__(self):
        self.cooldowns: Dict[str, Dict[str, datetime]] = {}
        self.cooldown_periods = {
            'mobilize': timedelta(days=1),
            'declare_war': timedelta(days=2),
            'issue_ultimatum': timedelta(days=1),
            'propose_alliance': timedelta(days=7),
            'offer_concessions': timedelta(days=3),
            'request_mediation': timedelta(days=3)
        }
        
    def is_action_available(self, country: str, action_type: str) -> bool:
        """Check if an action is available for a country."""
        if country not in self.cooldowns:
            return True
            
        if action_type not in self.cooldowns[country]:
            return True
            
        return datetime.now() >= self.cooldowns[country][action_type]
        
    def record_action(self, country: str, action_type: str):
        """Record that an action was taken by a country."""
        if country not in self.cooldowns:
            self.cooldowns[country] = {}
            
        cooldown_period = self.cooldown_periods.get(action_type, timedelta(days=1))
        self.cooldowns[country][action_type] = datetime.now() + cooldown_period
        
    def get_remaining_cooldown(self, country: str, action_type: str) -> timedelta:
        """Get the remaining cooldown time for an action."""
        if country not in self.cooldowns or action_type not in self.cooldowns[country]:
            return timedelta(0)
            
        remaining = self.cooldowns[country][action_type] - datetime.now()
        return max(remaining, timedelta(0)) 