from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.amal_category import AmalCategory
from app.seeds.factories import AmalCategoryFactory


async def create_category(
    session: AsyncSession,
    name: str,
    icon_id: Optional[int] = None,
) -> AmalCategory:
    """Create an amal category with the given name."""

    existing_category = await session.scalar(
        select(AmalCategory).where(AmalCategory.name == name)
    )
    if existing_category:
        return existing_category

    category = AmalCategoryFactory.build(name=name)
    if icon_id:
        category.iconId = icon_id

    session.add(category)
    await session.commit()
    await session.refresh(category)
    return category


async def create_categories(
    session: AsyncSession,
    names: list[str],
) -> list[AmalCategory]:
    """Create multiple amal categories with the given names."""

    categories = []
    for name in names:
        category = await create_category(session, name)
        categories.append(category)

    return categories


async def create_categories_amal(session: AsyncSession) -> list[AmalCategory]:
    """Create standard amal categories."""
    names = [
        "Намаз",
        "Дуа",
        "Зикр",
        "Садака",
    ]
    return await create_categories(session, names)
