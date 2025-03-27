from typing import Dict, List, Optional, TypedDict, Literal, Union

RelationType = Literal["Ally", "Enemy", "Neutral", "Tense"]
StateType = Literal["Peace", "War", "Mobilizing", "Civil Unrest", "Economic Crisis"]
ResourceType = Literal["Military", "Economic", "Diplomatic", "Cultural"]
EventCategory = Literal["Military", "Diplomatic", "Economic", "Cultural", "Internal"]

class ResourceLevel(TypedDict):
    value: float  # 0-100
    trend: float  # -1 to 1 indicating trend
    last_update: int  # turn number

class Sentiment(TypedDict):
    value: float  # -1 to 1
    history: List[float]  # historical values
    last_update: int  # turn number

class HistoricalEvent(TypedDict):
    turn: int
    category: EventCategory
    description: str
    impact: Dict[str, float]  # country -> impact value
    related_events: List[int]  # turn numbers of related events

class Event(TypedDict):
    turn: int
    text: str
    category: EventCategory
    impact: Dict[str, float]
    affected_countries: List[str]
    related_events: List[int] 