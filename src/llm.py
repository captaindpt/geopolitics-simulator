from typing import Dict, List, Optional
from openai import OpenAI

class LLMClient:
    def __init__(self, base_url: str, api_key: str):
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )
        
    def get_country_decision(self, 
                           country_name: str,
                           personality: str,
                           world_state: Dict,
                           recent_events: List[Dict]) -> str:
        """Get a decision from the LLM for a specific country"""
        # Build rich context for the LLM
        context = self._build_context(country_name, personality, world_state, recent_events)
        
        # Get decision from LLM
        response = self.client.chat.completions.create(
            model="llama-3-1-8b-instruct-mtb",
            messages=[{
                "role": "user",
                "content": context
            }],
            max_tokens=150,
            temperature=0.7,
            top_p=0.95,
            stream=False
        )
        
        return response.choices[0].message.content.strip()
    
    def resolve_conflicts(self, 
                         actions: List[Dict],
                         world_state: Dict) -> List[Dict]:
        """Use LLM to resolve conflicts between actions"""
        context = self._build_conflict_context(actions, world_state)
        
        response = self.client.chat.completions.create(
            model="llama-3-1-8b-instruct-mtb",
            messages=[{
                "role": "user",
                "content": context
            }],
            max_tokens=300,
            temperature=0.7,
            top_p=0.95,
            stream=False
        )
        
        # Parse and return resolved actions
        return self._parse_resolved_actions(response.choices[0].message.content)
    
    def _build_context(self, 
                      country_name: str,
                      personality: str,
                      world_state: Dict,
                      recent_events: List[Dict]) -> str:
        """Build rich context for country decision making"""
        country = world_state['countries'][country_name]
        
        context = f"""You are the leader of {country_name}, a {country['ideology']} nation with a {personality} personality.

Current State:
- Military Strength: {country['strength']}
- Current State: {country['state']}

Relationships:
"""
        # Add relationships
        for other, relation in country['relationships'].items():
            context += f"- {relation} with {other}\n"
            
        # Add recent events
        if recent_events:
            context += "\nRecent Events:\n"
            for event in recent_events[-3:]:  # Last 3 events
                context += f"- {event['text']}\n"
                
        # Add decision prompt
        context += """
Based on this situation, what action would you take? You can:
1. Declare war on another country
2. Form or break alliances
3. Mobilize forces
4. Take diplomatic actions
5. Make economic decisions
6. Or any other action you think appropriate

Respond with a clear, specific action. For example:
- "Declare war on France"
- "Form alliance with Russia"
- "Mobilize forces for defense"
- "Propose peace treaty to Britain"
"""
        return context
    
    def _build_conflict_context(self, 
                              actions: List[Dict],
                              world_state: Dict) -> str:
        """Build context for conflict resolution"""
        context = "You are a world mediator. The following actions have been proposed:\n\n"
        
        for action in actions:
            context += f"- {action['country']}: {action['text']}\n"
            
        context += "\nCurrent World State:\n"
        for country, state in world_state['countries'].items():
            context += f"- {country}: {state['state']}\n"
            
        context += """
Please resolve any conflicts between these actions and determine their outcomes.
For each action, specify:
1. Whether it succeeds or fails
2. Any consequences or reactions from other countries
3. How it affects the world state

Format your response as a list of resolved actions with their outcomes.
"""
        return context
    
    def _parse_resolved_actions(self, response: str) -> List[Dict]:
        """Parse the LLM's response into structured actions"""
        # This would parse the LLM's response into a list of actions with outcomes
        # For now, return a simple structure
        return [{
            "text": line.strip("- "),
            "outcome": "success"  # This would be determined by the LLM
        } for line in response.split("\n") if line.strip()] 