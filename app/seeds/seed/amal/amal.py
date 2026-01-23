import datetime
import random
from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.amal import Amal
from app.db.models.icon import Icon
from app.db.models.amal_category import AmalCategory
from app.seeds.factories import AmalFactory
from app.seeds.seed.amal.icon_amal import create_icons_amal
from app.seeds.seed.amal.amal_category import create_categories_amal


async def create_amal(
    session: AsyncSession,
    user_id: int,
    title: str,
    icon_id: Optional[int] = None,
    category_id: Optional[int] = None,
    date: Optional[datetime.date] = None,
    time: Optional[datetime.time] = None,
) -> Amal:
    """Create an amal with the given parameters."""
    
    amal = AmalFactory.build()
    amal.userId = user_id
    amal.title = title
    
    if icon_id:
        amal.iconId = icon_id
    if category_id:
        amal.categoryId = category_id
    if date:
        amal.date = date
    if time:
        amal.time = time
    
    session.add(amal)
    await session.commit()
    await session.refresh(amal)
    return amal


async def create_amals_with_icons_and_categories(
    session: AsyncSession,
    user_id: int,
    count: int = 10,
) -> list[Amal]:
    """Create multiple amals with icons and categories."""
    
    icons = await create_icons_amal(session)
    categories = await create_categories_amal(session)
    
    amal_titles = [
        "Утренний намаз",
        "Зухр намаз",
        "Аср намаз",
        "Магриб намаз",
        "Иша намаз",
        "Чтение Корана (1 страница)",
        "Утренние азкары",
        "Вечерние азкары",
        "Истигфар 100 раз",
        "Салават 100 раз",
        "Дуа после намаза",
        "Садака",
        "Помощь нуждающимся",
        "Навестить больного",
        "Учить суру",
    ]
    
    amals = []
    for _ in range(count):
        title = random.choice(amal_titles)
        icon = random.choice(icons) if random.random() > 0.3 else None
        category = random.choice(categories) if random.random() > 0.3 else None
        
        amal = AmalFactory.build(
            icon=icon,
            category=category,
        )
        amal.userId = user_id
        amal.title = title
        
        session.add(amal)
        amals.append(amal)
    
    await session.commit()
    
    for amal in amals:
        await session.refresh(amal)
    
    return amals
