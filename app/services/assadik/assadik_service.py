from uuid import UUID

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_deepseek import ChatDeepSeek

from app.api.v1.schemas.assadik.message import MessageCreate, MessageRead
from app.core.config import settings
from app.db.cruds.assadik_repository import AssadikRepository
from app.db.models.enums import Role
from app.services.assadik.constants import SYSTEM_PROMPT
from app.utils.structlog_config import logger


class AssadikService:
    def __init__(self, repo: AssadikRepository):
        self._repo = repo

    @staticmethod
    async def __generate_response(message: str) -> str:
        """
        Generate a response from the assistant based on the provided message.

        Args:
            message (str): The content of the user's message.

        Returns:
            str: The generated response from the assistant.
        """
        chat = ChatDeepSeek(
            model=settings.ai.model,
            api_key=settings.ai.api_key,
            temperature=0.7,
        )

        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=message),
        ]

        response = await chat.ainvoke(messages)

        return response.content

    async def chat(self, *, message: MessageCreate, user_id: UUID) -> MessageRead:
        """
        Sends a message from the user to the assistant and returns the assistant's response.

        Args:
            message (MessageCreate): The message sent by the user.
            user_id (UUID): The unique identifier of the user sending the message.

        Returns:
            MessageRead: The response message from the assistant, including its metadata.

        Raises:
            Any exceptions from the repository or language model will be propagated. Handles
            database persistence for both user and assistant messages.
        """
        await self._repo.add_message(
            content=message.content,
            role=Role.USER,
            user_id=user_id,
        )

        try:
            response = await self.__generate_response(message.content)
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            response = "Извините, произошла ошибка. Попробуйте позже."

        response_message = await self._repo.add_message(
            content=response,
            role=Role.ASSISTANT,
            user_id=user_id,
        )

        return MessageRead(
            id=response_message.id,
            content=response_message.content,
            createdAt=response_message.createdAt,
            role=response_message.role,
        )
