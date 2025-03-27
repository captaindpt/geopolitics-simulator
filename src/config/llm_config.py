from dataclasses import dataclass
from typing import Optional

@dataclass
class LLMConfig:
    model: str = "llama-3-1-8b-instruct-mtb"
    base_url: str = "https://vmjps1ofbtvn2w43.us-east-1.aws.endpoints.huggingface.cloud/v1"
    max_tokens: int = 150
    temperature: Optional[float] = None
    top_p: Optional[float] = None
    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None
    stream: bool = False 