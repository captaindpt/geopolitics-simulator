from typing import Optional, List, Dict, Any
from openai import OpenAI
from .base_agent import Agent
from src.models.world import World
from src.config.llm_config import LLMConfig

class LLMAgent(Agent):
    def __init__(self, country_name: str, personality: str, api_key: str, config: Optional[LLMConfig] = None):
        """
        Initialize an LLM-based agent
        
        Args:
            country_name: Name of the country this agent controls
            personality: "Aggressive", "Cautious", or "Neutral"
            api_key: HuggingFace API key
            config: Optional LLM configuration
        """
        super().__init__(country_name, personality)
        self.config = config or LLMConfig()
        self.client = OpenAI(
            base_url=self.config.base_url,
            api_key=api_key
        )
        self.recent_actions: List[Dict[str, Any]] = []  # Track recent actions with narratives
        
    def decide(self, world: World) -> Dict[str, Any]:
        """
        Use LLM to make decisions based on perception
        
        Args:
            world: Current world state
            
        Returns:
            Dict containing decision and narrative
        """
        perception = self.perceive(world)
        
        # Add recent actions to perception
        if self.recent_actions:
            recent_narratives = [action["narrative"] for action in self.recent_actions[-3:]]
            perception += f"\n\nYour recent actions:\n" + "\n".join(recent_narratives)
        
        # Get country's ideology from world state
        country = world.get_country(self.country_name)
        if not country:
            return {
                "action": "Do nothing",
                "narrative": f"Unable to find country data for {self.country_name}"
            }
            
        prompt = self._build_decision_prompt(perception, country.ideology)
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                max_tokens=500,  # Increased for narrative
                temperature=0.8,  # Slightly higher for more creative writing
                top_p=0.95,
                stream=False
            )
            
            if response.choices:
                decision_text = response.choices[0].message.content
                print(f"Raw decision for {self.country_name}: {decision_text}")  # Debug output
                
                # Parse the decision into action and narrative
                decision = self._parse_decision(decision_text)
                
                # Check if this is a repetitive action
                if decision["action"] in [a["action"] for a in self.recent_actions]:
                    # If repeating Mobilize forces, just do nothing
                    if decision["action"] == "Mobilize forces":
                        return {
                            "action": "Do nothing",
                            "narrative": f"As tensions remain high but no immediate action is required, {self.country_name} maintains its current position."
                        }
                    # For other actions, only allow if it's been 3 or more turns
                    if len(self.recent_actions) < 3:
                        return {
                            "action": "Do nothing",
                            "narrative": f"Given recent similar actions, {self.country_name} chooses to maintain its current stance."
                        }
                
                # Add to recent actions
                self.recent_actions.append(decision)
                if len(self.recent_actions) > 5:  # Keep last 5 actions
                    self.recent_actions = self.recent_actions[-5:]
                    
                return decision
            else:
                print(f"No response from API for {self.country_name}")
                return {
                    "action": "Do nothing",
                    "narrative": f"Unable to reach a clear decision, {self.country_name} maintains its current position."
                }
            
        except Exception as e:
            print(f"Error getting LLM decision for {self.country_name}: {e}")
            return {
                "action": "Do nothing",
                "narrative": f"Due to internal deliberations, {self.country_name} maintains its current position."
            }
            
    def _build_decision_prompt(self, perception: str, ideology: str) -> str:
        """Build the prompt for the LLM"""
        return f"""You are the leader of {self.country_name}, a {ideology} nation with a {self.personality} personality. 
You are making decisions that will shape the course of history. Consider your nation's interests, alliances, and the broader geopolitical landscape.

Current situation:
{perception}

Based on this situation, describe your next action and its rationale. Consider:
- The historical context and precedents
- The impact on your people and allies
- The long-term strategic implications
- The personal and political consequences

Your response should be a natural narrative that includes:
1. Your decision and its immediate action
2. Your reasoning and strategic thinking
3. How you expect other nations to react
4. Any specific conditions or terms you're setting

Example response:
"Given the growing tensions and our historical rivalry with France, I have decided to mobilize our forces along the border. This is a defensive measure to protect our interests, though I expect it will be interpreted as provocative by some. We must be prepared for any response from our neighbors."

Remember to maintain a historically appropriate tone and consider the personality and ideology of your nation."""
        
    def _parse_decision(self, decision_text: str) -> Dict[str, Any]:
        """Parse the LLM's narrative response into action and narrative"""
        # Extract the core action from the narrative
        action = "Do nothing"  # Default action
        
        # Look for key action phrases
        if "declare war" in decision_text.lower():
            action = "Declare war"
        elif "mobilize" in decision_text.lower():
            action = "Mobilize forces"
        elif "alliance" in decision_text.lower():
            action = "Propose alliance"
        elif "help" in decision_text.lower():
            action = "Help"
        elif "peace" in decision_text.lower():
            action = "Sue for peace"
            
        # Clean up the narrative
        narrative = decision_text.strip()
        
        # Remove any leading/trailing whitespace and normalize
        narrative = " ".join(narrative.split())
        
        return {
            "action": action,
            "narrative": narrative
        } 