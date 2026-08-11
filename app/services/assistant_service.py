import logging

from app.models.request import Request
from app.tools.calculator import add
from app.tools.text_tool import to_upper, to_lower, get_length

logger = logging.getLogger(__name__)

class AssistantService:

    def process(self, request: Request) -> str:
        
        logger.info(
            "Processing action: %s",
            request.action
        )

        if request.action == "upper":
            return to_upper(request.content)

        if request.action == "lower":
            return to_lower(request.content)

        if request.action == "length":
            return str(get_length(request.content))

        if request.action == "add":
            try:
                parts = request.content.split(" ")

                a = float(parts[0])
                b = float(parts[1])
                result = add(a, b)
                logger.info(
                    "Calculation completed: %s + %s = %s",
                    a, b, result,
                )

                return str(result)
            except (ValueError, IndexError):
                logger.exception(
                    "Invalid calculator input: %s",
                    request.content,
                )

                return "Invalid numbers"
        logger.warning(
            "Unknown action: %s",
            request.action,
        )

        return "Unknown action"

class UnknowActionError(Exception): 
    pass


            