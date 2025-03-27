from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from .base_action import Action

if TYPE_CHECKING:
    from src.models.world import World
    from src.models.country import Country

class DeclareWarAction(Action):
    def execute(self, world: 'World') -> bool:
        """Execute war declaration between countries"""
        if not self.target:
            return False
            
        # Prevent declaring war on self
        if self.source == self.target:
            return False
            
        source_country = world.get_country(self.source)
        target_country = world.get_country(self.target)
        
        if not source_country or not target_country:
            return False
            
        # Check if already at war
        if source_country.get_relationship(self.target) == "Enemy":
            return False
            
        # Change relationships
        source_country.set_relationship(self.target, "Enemy")
        target_country.set_relationship(self.source, "Enemy")
        
        # Change states
        source_country.set_state("War")
        target_country.set_state("War")
        
        # Update sentiments
        source_country.update_sentiment(self.target, -0.5, world.turn)
        target_country.update_sentiment(self.source, -0.5, world.turn)
        
        # Record event with impact
        world.add_event({
            "text": f"{self.source} declared war on {self.target}",
            "category": "Military",
            "impact": {
                self.source: -0.2,  # Economic impact
                self.target: -0.2
            },
            "affected_countries": [self.source, self.target]
        })
        return True

class ProposeAllianceAction(Action):
    def execute(self, world: 'World') -> bool:
        """Execute alliance proposal between countries"""
        if not self.target:
            return False
            
        source_country = world.get_country(self.source)
        target_country = world.get_country(self.target)
        
        if not source_country or not target_country:
            return False
            
        # Check if alliance would be accepted
        if self._would_accept_alliance(source_country, target_country):
            source_country.set_relationship(self.target, "Ally")
            target_country.set_relationship(self.source, "Ally")
            
            # Update sentiments
            source_country.update_sentiment(self.target, 0.3, world.turn)
            target_country.update_sentiment(self.source, 0.3, world.turn)
            
            # Record event with impact
            world.add_event({
                "text": f"{self.source} and {self.target} formed an alliance",
                "category": "Diplomatic",
                "impact": {
                    self.source: 0.1,  # Diplomatic boost
                    self.target: 0.1
                },
                "affected_countries": [self.source, self.target]
            })
            return True
        else:
            # Record rejected proposal
            world.add_event({
                "text": f"{self.target} rejected {self.source}'s alliance proposal",
                "category": "Diplomatic",
                "impact": {
                    self.source: -0.1,  # Diplomatic setback
                    self.target: -0.05
                },
                "affected_countries": [self.source, self.target]
            })
            return False
            
    def _would_accept_alliance(self, source: 'Country', target: 'Country') -> bool:
        """Determine if target country would accept alliance"""
        # Accept if same ideology
        if source.ideology == target.ideology:
            return True
            
        # Accept if have common enemies
        source_enemies = {name for name, rel in source.relationships.items() 
                        if rel == "Enemy"}
        target_enemies = {name for name, rel in target.relationships.items() 
                        if rel == "Enemy"}
        
        return bool(source_enemies & target_enemies)  # Have common enemies

class HelpAction(Action):
    def execute(self, world: 'World') -> bool:
        """Execute help action for a country at war"""
        if not self.target:
            return False
            
        source_country = world.get_country(self.source)
        target_country = world.get_country(self.target)
        
        if not source_country or not target_country:
            return False
            
        # Can only help if target is at war
        if target_country.state != "War":
            return False
            
        # Find target's enemies
        target_enemies = [name for name, rel in target_country.relationships.items() 
                        if rel == "Enemy"]
        
        if not target_enemies:
            return False
            
        # Join war against first enemy
        enemy = target_enemies[0]
        enemy_country = world.get_country(enemy)
        
        if not enemy_country:
            return False
            
        # Change relationships
        source_country.set_relationship(enemy, "Enemy")
        enemy_country.set_relationship(self.source, "Enemy")
        source_country.set_relationship(self.target, "Ally")
        target_country.set_relationship(self.source, "Ally")
        
        # Change state
        source_country.set_state("War")
        
        # Update sentiments
        source_country.update_sentiment(self.target, 0.4, world.turn)
        target_country.update_sentiment(self.source, 0.4, world.turn)
        source_country.update_sentiment(enemy, -0.4, world.turn)
        enemy_country.update_sentiment(self.source, -0.4, world.turn)
        
        # Record event with impact
        world.add_event({
            "text": f"{self.source} joined {self.target}'s war against {enemy}",
            "category": "Military",
            "impact": {
                self.source: -0.15,  # Economic impact
                self.target: 0.1,    # Military boost
                enemy: -0.1          # Military setback
            },
            "affected_countries": [self.source, self.target, enemy]
        })
        return True 