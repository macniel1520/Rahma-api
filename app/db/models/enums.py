import enum
from sqlalchemy.dialects.postgresql import UUID as PG_UUID

UUID_PK = PG_UUID(as_uuid=True)


class Role(enum.Enum):
    ASSISTANT = "assistant"
    USER = "user"


class Category(enum.Enum):
    HAJJ = "hajj"
    UMRAH = "umrah"
    HISTORY = "history"


class CostLevel(enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ReccuringRule(enum.Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
