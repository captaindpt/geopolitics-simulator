from typing import Optional, Dict
from models.world import World
from actions.base_action import BaseAction
from actions.action_factory import ActionFactory
from agents.base_agent import Agent, PersonalityType

class LLMAgent(Agent):
    """Agent that uses LLM to make decisions."""
    
    def __init__(self, name: str, personality: PersonalityType):
        super().__init__(name, personality)
        self.action_factory = ActionFactory()
        
    def decide(self, world: World) -> Optional[BaseAction]:
        """Make a decision based on the current world state."""
        perception = self._generate_perception(world)
        
        # Generate decision based on historical context and personality
        decision = self._generate_decision(perception)
        
        # Create and return action
        return self.action_factory.create_action(self.name, decision)
        
    def _generate_decision(self, perception: Dict) -> str:
        """Generate a decision based on the agent's perception."""
        # Historical context for each country
        contexts = {
            'AUSTRIA': "Must respond strongly to Serbian threats while maintaining alliance with Germany",
            'GERMANY': "Must support Austrian ally while preparing for potential conflict with Russia and France",
            'RUSSIA': "Must protect Serbian interests while preparing for potential conflict with Austria and Germany",
            'FRANCE': "Must support Russian ally while watching German military buildup",
            'BRITAIN': "Must maintain balance of power in Europe while protecting Belgian neutrality",
            'ITALY': "Must carefully balance alliance commitments with territorial ambitions",
            'SERBIA': "Must maintain sovereignty while seeking protection from Russian ally"
        }
        
        # Get country's context
        context = contexts.get(self.name, "")
        
        # Make decision based on context and current situation
        if self.name == 'AUSTRIA' and 'Archduke Franz Ferdinand assassinated' in perception['recent_events']:
            return "Issue ultimatum to SERBIA because they must be held accountable for the assassination of Archduke Franz Ferdinand"
            
        if self.name == 'GERMANY' and any('AUSTRIA' in event and 'ultimatum' in event.lower() for event in perception['recent_events']):
            return "Mobilize forces because we must support our Austrian allies against Serbian aggression"
            
        if self.name == 'RUSSIA' and any('SERBIA' in event and 'ultimatum' in event.lower() for event in perception['recent_events']):
            return "Mobilize forces because we must protect our Serbian brothers from Austrian aggression"
            
        if self.name == 'SERBIA' and any('ultimatum' in event.lower() for event in perception['recent_events']):
            return "Request mediation from RUSSIA because Austrian demands threaten our sovereignty"
            
        if perception['global_tension'] > 0.7:
            if self.personality == PersonalityType.AGGRESSIVE:
                return "Declare war on " + (perception['enemies'][0] if perception['enemies'] else "Do nothing")
            elif self.personality == PersonalityType.DIPLOMATIC:
                return "Request mediation from " + (perception['allies'][0] if perception['allies'] else "Do nothing")
                
        return "Do nothing because the situation requires careful observation"
        
    def _generate_perception(self, world: World) -> Dict:
        """Generate a perception of the world state."""
        return {
            'global_tension': world.global_tension,
            'active_conflicts': list(world.active_conflicts),
            'recent_events': world.events,
            'allies': list(world.get_allies(self.name)),
            'enemies': list(world.get_enemies(self.name))
        } 