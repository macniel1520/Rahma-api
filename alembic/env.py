import asyncio
from logging.config import fileConfig

from asyncpg.exceptions import CannotConnectNowError
from sqlalchemy.exc import OperationalError

from alembic import context
from app.core.config import settings
from app.db.engine import engine
from app.db.models.base import Base

config = context.config

config.set_main_option("sqlalchemy.url", str(settings.db.root))

fileConfig(config.config_file_name)

target_metadata = Base.metadata


async def wait_for_db(engine, retries=10, delay=3):
    for attempt in range(retries):
        try:
            async with engine.connect():
                print("База данных доступна.")
                return
        except (OperationalError, CannotConnectNowError):
            print(
                f"Попытка {attempt + 1} не удалась, база данных еще не доступна. Повтор через {delay} секунд."
            )
            await asyncio.sleep(delay)
    raise Exception("Не удалось подключиться к базе данных после нескольких попыток.")


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    await wait_for_db(engine)

    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
