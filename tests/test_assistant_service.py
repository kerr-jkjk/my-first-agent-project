from app.models.request import Request
from app.services.assistant_service import AssistantService

def test_uper() -> None:
    service = AssistantService()

    request = Request(
        action="upper",
        content="hello world"
    )
    result = service.process(request)
    assert result == "HELLO WORLD"

def test_lower() -> None:
    service = AssistantService()

    request = Request(
        action="lower",
        content="HELLO WORLD"
    )
    result = service.process(request)
    assert result == "hello world"

def test_add() -> None:
    service = AssistantService()

    request = Request(
        action="add",
        content="2 3"
    )
    result = service.process(request)

    assert result == "5.0"