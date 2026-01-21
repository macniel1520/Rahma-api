import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base, TimestampMixin
from app.db.models.enums import UUID_PK, ReccuringRule

if TYPE_CHECKING:
    from app.db.models.route import Route


class AmalTemplate(Base, TimestampMixin):
    __tablename__ = "amal_template"

    id: Mapped[uuid.UUID] = mapped_column(UUID_PK, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    reccuringRule: Mapped[ReccuringRule] = mapped_column(
        Enum(ReccuringRule, name="reccuring_rule_enum"), nullable=False
    )

    routeId: Mapped[uuid.UUID] = mapped_column(
        UUID_PK, ForeignKey("route.id", ondelete="CASCADE"), nullable=False
    )
    route: Mapped["Route"] = relationship("Route", back_populates="amal_templates")
