import enum

from sqlalchemy.dialects.postgresql import UUID as PG_UUID

UUID_PK = PG_UUID(as_uuid=True)


class Role(str, enum.Enum):
    ASSISTANT = "assistant"
    USER = "user"


class Category(str, enum.Enum):
    HAJJ = "hajj"
    UMRAH = "umrah"
    HISTORY = "history"


class CostLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ReccuringRule(str, enum.Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    YEARLY = "yearly"
