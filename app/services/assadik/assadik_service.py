from uuid import UUID

from app.api.v1.schemas.assadik.message import MessageCreate, MessageRead, MessageUI
from app.db.cruds.assadik_repository import AssadikRepository
from app.db.cruds.route_search_repository import SqlAlchemyRouteSearchRepository
from app.db.models.enums import Role
from app.services.assadik.ai_agent_service import AIAgentService
from app.utils.structlog_config import logger


class AssadikService:
    def __init__(
        self,
        repo: AssadikRepository,
        route_search_repo: SqlAlchemyRouteSearchRepository,
    ):
        self._repo = repo
        self._ai_agent = AIAgentService(route_search_repo)

    async def chat(self, *, message: MessageCreate, user_id: UUID) -> MessageRead:
        """
        Sends a message from the user to the assistant and returns the assistant's response with UI data.

        Args:
            message (MessageCreate): The message sent by the user.
            user_id (UUID): The unique identifier of the user sending the message.

        Returns:
            MessageRead: The response message from the assistant, including its metadata and UI data.

        Raises:
            Any exceptions from the repository or AI agent will be propagated. Handles
            database persistence for both user and assistant messages.
        """
        # Сохраняем сообщение пользователя
        await self._repo.add_message(
            content=message.content,
            role=Role.USER,
            user_id=user_id,
        )

        try:
            # Обрабатываем сообщение через AI агента
            agent_result = await self._ai_agent.process_message(message.content)

            response_content = agent_result["content"]
            ui_data = agent_result["ui"]

            # Преобразуем UI данные в Pydantic модель
            ui_model = None
            if ui_data:
                ui_model = MessageUI(**ui_data)

        except Exception as e:
            logger.error(f"Error processing message with AI agent: {e}")
            response_content = "Извините, произошла ошибка. Попробуйте позже."
            ui_model = None

        # Сохраняем ответ ассистента
        response_message = await self._repo.add_message(
            content=response_content,
            role=Role.ASSISTANT,
            user_id=user_id,
        )

        return MessageRead(
            id=response_message.id,
            content=response_message.content,
            createdAt=response_message.createdAt,
            role=response_message.role,
            ui=ui_model,
        )
