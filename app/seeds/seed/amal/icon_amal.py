from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.icon import Icon
from app.seeds.factories import IconFactory


async def create_icon(
    session: AsyncSession,
    url: str,
    name: Optional[str] = None,
) -> Icon:
    """Create an icon with the given URL."""

    existing_icon = await session.scalar(select(Icon).where(Icon.url == url))
    if existing_icon:
        return existing_icon

    icon = IconFactory.build(url=url)
    if name:
        icon.name = name

    session.add(icon)
    await session.commit()
    await session.refresh(icon)
    return icon


async def create_icons(
    session: AsyncSession,
    urls: list[str],
) -> list[Icon]:
    """Create multiple icons with the given URLs."""

    icons = []
    for url in urls:
        icon = await create_icon(session, url)
        icons.append(icon)

    return icons


async def create_icons_amal(session: AsyncSession) -> list[Icon]:
    urls = [
        "https://s3.geometria.ru/rahma-test/amal-icons/Arrow.svg",
        "https://s3.geometria.ru/rahma-test/amal-icons/At.svg",
        "https://s3.geometria.ru/rahma-test/amal-icons/Bell.svg",
        "https://s3.geometria.ru/rahma-test/amal-icons/Calendar.svg",
        "https://s3.geometria.ru/rahma-test/amal-icons/Chat.svg",
        "https://s3.geometria.ru/rahma-test/amal-icons/Clock.svg",
        "https://s3.geometria.ru/rahma-test/amal-icons/Credit%20Card.svg",
        "https://s3.geometria.ru/rahma-test/amal-icons/Hajj.svg",
        "https://s3.geometria.ru/rahma-test/amal-icons/History.svg",
        "https://s3.geometria.ru/rahma-test/amal-icons/Home.svg",
        "https://s3.geometria.ru/rahma-test/amal-icons/Hotel.svg",
        "https://s3.geometria.ru/rahma-test/amal-icons/Map.svg",
        "https://s3.geometria.ru/rahma-test/amal-icons/Microphone.svg",
        "https://s3.geometria.ru/rahma-test/amal-icons/Mosque.svg",
        "https://s3.geometria.ru/rahma-test/amal-icons/Umra.svg",
        "https://s3.geometria.ru/rahma-test/amal-icons/Vibrate.svg",
    ]
    return await create_icons(session, urls)
