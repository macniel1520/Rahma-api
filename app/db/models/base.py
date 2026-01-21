import datetime

from sqlalchemy import DateTime, text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=text("TIMEZONE('Europe/Moscow', NOW())")
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=text("TIMEZONE('Europe/Moscow', NOW())"),
        onupdate=func.now(),
    )
