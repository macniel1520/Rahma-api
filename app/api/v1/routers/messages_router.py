from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.schemas.assadik.message import MessageCreate, MessageRead
from app.db.cruds.assadik_repository import SqlAlchemyAssadikRepository
from app.db.engine import get_session
from app.docs.responses import unauthorized_response
from app.services.assadik.assadik_service import AssadikService
from app.services.auth.current_user import CurrentUser

router = APIRouter(prefix="/messages", tags=["messages"])


def get_assadik_service(session: AsyncSession = Depends(get_session)) -> AssadikService:
    return AssadikService(repo=SqlAlchemyAssadikRepository(session=session))


@router.post(
    "",
    response_model=MessageRead,
    summary="Отправить сообщение",
    description=(
        "Отправляет сообщение в чат с ассадиком.\n\n"
        "Поле `content` должно быть не пустым и не более 1000 символов.\n\n"
        "При ошибке генерации ответа возвращается сообщение `MessageRead` с полем `content`: **Извините, произошла ошибка. Попробуйте позже.**"
    ),
    response_description="Ответ от ассадика",
    status_code=status.HTTP_201_CREATED,
    responses={
        **unauthorized_response,  # noqa F405
    },
)
async def send_message(
    message: MessageCreate,
    current_user: CurrentUser,
    service: AssadikService = Depends(get_assadik_service),
) -> MessageRead:
    return await service.chat(message=message, user_id=current_user.id)
