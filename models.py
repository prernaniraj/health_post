from typing import TypedDict, Annotated, Literal
from dataclasses import dataclass
import operator

class AppState(TypedDict):
    messages: Annotated[list, operator.add]
    topic: str
    platform: Literal["instagram", "facebook", "linkedin"]
    post_content: str
    error: str

@dataclass
class PostRequest:
    topic: str
    platform: str
    user_id: str = "anonymous"

@dataclass
class PostResponse:
    content: str
    platform: str
    topic: str
    success: bool
    error: str = ""