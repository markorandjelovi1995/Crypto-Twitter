from typing import Any, Dict
from dataclasses import dataclass


@dataclass
class TwitterCredential:
    consumer_key: str
    consumer_secret: str
    access_token: str
    access_token_secret: str


StatusAsDict = Dict[str, Any]
