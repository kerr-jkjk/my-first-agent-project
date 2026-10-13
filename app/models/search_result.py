from dataclasses import dataclass

@dataclass
class SearchResult:
    source: str
    keyword: str
    items: list[str]
    error: str | None = None