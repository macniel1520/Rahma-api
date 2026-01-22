from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


def get_sync_engine():
    """Create sync SQLAlchemy engine for SQLAdmin."""
    async_uri = settings.db.uri
    sync_uri = async_uri.replace("postgresql+asyncpg://", "postgresql://")

    return create_engine(sync_uri, echo=False, future=True)


def get_sync_session():
    """Create sync session factory for SQLAdmin."""
    engine = get_sync_engine()
    return sessionmaker(bind=engine, expire_on_commit=False)


sync_engine = get_sync_engine()
