import asyncio
import datetime
import os
import random

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import AsyncSessionLocal
from app.db.models.amal_completion import AmalCompletion
from app.db.models.user import User
from app.seeds.factories import AmalCompletionFactory
from app.seeds.seed.amal.icon_amal import create_icons_amal
from app.seeds.seed.amal.amal_category import create_categories_amal
from app.seeds.seed.amal.amal import create_amals_with_icons_and_categories
from app.seeds.seed.sabil import (
    create_countries_sabil,
    create_routes_sabil,
    create_route_images_sabil,
    create_restaurants_sabil,
    create_hotels_sabil,
    create_amal_templates_sabil,
)
from app.services.auth.passwords import hash_password

SEED_USER_EMAIL = "seed@seed.com"


async def seed_sabil(session: AsyncSession) -> None:
    """Seed sabil data: countries, routes, images, restaurants, hotels, amal templates."""
    
    # 1. Создаём страны (нет зависимостей)
    countries = await create_countries_sabil(session)
    print(f"Created {len(countries)} countries")
    
    # 2. Создаём маршруты (зависят от Country)
    routes_map = await create_routes_sabil(session, countries)
    all_routes = [route for routes in routes_map.values() for route in routes]
    print(f"Created {len(all_routes)} routes")
    
    # 3. Создаём изображения маршрутов (зависят от Route)
    route_images = await create_route_images_sabil(session, all_routes)
    print(f"Created {len(route_images)} route images")
    
    # 4. Создаём рестораны (зависят от Route)
    restaurants = await create_restaurants_sabil(session, all_routes)
    print(f"Created {len(restaurants)} restaurants")
    
    # 5. Создаём отели (зависят от Route)
    hotels = await create_hotels_sabil(session, all_routes)
    print(f"Created {len(hotels)} hotels")
    
    # 6. Создаём шаблоны амалей (зависят от Route)
    amal_templates = await create_amal_templates_sabil(session, all_routes)
    print(f"Created {len(amal_templates)} amal templates")


async def seed_amals(session: AsyncSession) -> None:
    """Seed amals data: icons, categories, amals for test user."""
    
    # Получаем или создаём тестового пользователя
    seed_user = await session.scalar(
        select(User).where(User.email == SEED_USER_EMAIL)
    )
    if not seed_user:
        seed_user = User(
            email=SEED_USER_EMAIL,
            password=hash_password("seedseed"),
            isVerified=True,
            isActive=True,
            name="Seed User",
        )
        session.add(seed_user)
        await session.commit()
        await session.refresh(seed_user)
    
    # Создаём иконки для амалей
    icons = await create_icons_amal(session)
    print(f"Created {len(icons)} icons")
    
    # Создаём категории амалей
    categories = await create_categories_amal(session)
    print(f"Created {len(categories)} categories")
    
    # Создаём амали для тестового пользователя
    amals = await create_amals_with_icons_and_categories(
        session,
        user_id=seed_user.id,
        count=random.randint(5, 10),
    )
    print(f"Created {len(amals)} amals")
    
    # Создаём записи о выполнении амалей
    completions_count = 0
    for amal in amals:
        for days_ago in range(random.randint(0, 5)):
            if random.random() > 0.4:
                completion_date = datetime.date.today() - datetime.timedelta(
                    days=days_ago
                )
                completion = AmalCompletionFactory.build(
                    date=completion_date,
                    completedAt=datetime.datetime.now()
                    - datetime.timedelta(days=days_ago),
                )
                completion.amalId = amal.id
                completion.userId = seed_user.id
                session.add(completion)
                completions_count += 1
    
    await session.commit()
    print(f"Created {completions_count} amal completions")


async def seed(session: AsyncSession) -> None:
    env = os.getenv("ENV", "dev")
    if env == "prod":
        raise RuntimeError("Seeding запрещен в prod окружении")

    # Создаём sabil данные (страны, маршруты, рестораны, отели и т.д.)
    await seed_sabil(session)
    
    # Создаём amal данные (иконки, категории, амали для тестового пользователя)
    await seed_amals(session)


async def seed_db() -> None:
    async with AsyncSessionLocal() as session:
        await seed(session)
        print("Seed completed")


if __name__ == "__main__":
    asyncio.run(seed_db())
