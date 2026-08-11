from dataclasses import dataclass

@dataclass
class Request:
    action: str
    content: str