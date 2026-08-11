import logging

from app.config import APP_NAME, LOG_LEVEL, MY_API_KEY
from app.services.assistant_service import AssistantService
from app.models.request import Request

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def parse_input(user_input: str) -> Request:
    parts = user_input.split(maxsplit=1)

    action = parts[0]

    content = (
        parts[1]
        if len(parts) > 1
        else ""
    )

    return Request(action = action, content = content)




def main() -> None:

    logger.info("%s started.", APP_NAME)

    service = AssistantService()

    print(f"{APP_NAME} started.")

    while True:

        user_input = input("> ").strip()

        if user_input == "exit":
            print("Bye!")
            break

        if not user_input:
            continue

        request = parse_input(user_input)

        result = service.process(request)

        print(f"Result: {result}")



if __name__ == "__main__":
    main()
    
