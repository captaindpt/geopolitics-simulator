from typing import Optional, List
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
        self.recent_actions: List[str] = []  # Track recent actions
        
    def decide(self, world: World) -> str:
        """
        Use LLM to make decisions based on perception
        
        Args:
            world: Current world state
            
        Returns:
            Decision string describing chosen action
        """
        perception = self.perceive(world)
        
        # Add recent actions to perception
        if self.recent_actions:
            perception += f"\n\nYour recent actions: {', '.join(self.recent_actions[-3:])}"
        
        prompt = self._build_decision_prompt(perception)
        
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature if self.config.temperature is not None else 0.7,
                top_p=self.config.top_p if self.config.top_p is not None else 0.95,
                stream=False
            )
            
            if response.choices:
                decision = response.choices[0].message.content
                # Clean up the decision text
                decision = decision.strip().split('\n')[0]  # Take first line only
                print(f"Raw decision for {self.country_name}: {decision}")  # Debug output
                
                # Validate and clean decision
                decision = self._validate_decision(decision.strip())
                
                # Check if this is a repetitive action
                if decision in self.recent_actions:
                    # If repeating Mobilize forces, just do nothing
                    if decision == "Mobilize forces":
                        return "Do nothing"
                    # For other actions, only allow if it's been 3 or more turns
                    if len(self.recent_actions) < 3:
                        return "Do nothing"
                
                # Add to recent actions
                self.recent_actions.append(decision)
                if len(self.recent_actions) > 5:  # Keep last 5 actions
                    self.recent_actions = self.recent_actions[-5:]
                    
                return decision
            else:
                print(f"No response from API for {self.country_name}")
                return "Do nothing"
            
        except Exception as e:
            print(f"Error getting LLM decision for {self.country_name}: {e}")
            return "Do nothing"
            
    def _build_decision_prompt(self, perception: str) -> str:
        """Build the prompt for the LLM"""
        return f"""You are a geopolitical decision-making AI. Your task is to make a single, clear decision based on the given situation.

You are the leader of {self.country_name} with a {self.personality} personality.

Current situation:
{perception}

IMPORTANT: You must respond with EXACTLY ONE of these actions, with no additional text or explanation:
1. Declare war on [country] - Only if not already at war with them
2. Propose alliance to [country] - Only if not already allied
3. Help [country] against their enemies - Only if they are at war
4. Mobilize forces - Only if not done recently
5. Sue for peace with [country] - Only if at war with them
6. Do nothing - If no other action makes sense

Example valid responses:
- Declare war on Russia
- Propose alliance to China
- Help France against their enemies
- Mobilize forces
- Sue for peace with Germany
- Do nothing

Your response must be exactly one of these actions, with the appropriate country name if needed. Do not add any other text, explanations, or notes.
Consider your recent actions to avoid repetition."""
        
    def _validate_decision(self, decision: str) -> str:
        """Validate and clean up the LLM's decision"""
        valid_actions = [
            "Declare war on",
            "Propose alliance to",
            "Help",
            "Mobilize forces",
            "Sue for peace with",
            "Do nothing"
        ]
        
        print(f"Validating decision for {self.country_name}: {decision}")  # Debug output
        
        # Clean up common variations and extra text
        decision = decision.strip()
        decision = decision.replace("I choose to ", "")
        decision = decision.replace("I will ", "")
        decision = decision.replace("Let's ", "")
        decision = decision.replace("Note:", "")
        decision = decision.replace("This situation", "")
        decision = decision.replace("please respond accordingly", "")
        decision = decision.replace("accordingly", "")
        decision = decision.replace(".", "")
        
        # Remove any leading/trailing whitespace
        decision = decision.strip()
        
        print(f"Cleaned decision for {self.country_name}: {decision}")  # Debug output
        
        # Check if the decision starts with any valid action
        for action in valid_actions:
            if decision.startswith(action):
                print(f"Valid decision found for {self.country_name}: {decision}")  # Debug output
                return decision
                
        print(f"Invalid decision format for {self.country_name}: {decision}")  # Debug output
        return "Do nothing" 