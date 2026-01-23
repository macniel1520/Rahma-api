import asyncio
import datetime
import os
import random

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import AsyncSessionLocal
from app.db.models.amal import Amal
from app.db.models.amal_category import AmalCategory
from app.db.models.amal_completion import AmalCompletion
from app.db.models.amal_template import AmalTemplate
from app.db.models.country import Country
from app.db.models.hotel import Hotel
from app.db.models.icon import Icon
from app.db.models.restaurant import Restaurant
from app.db.models.route import Route
from app.db.models.route_image import RouteImage
from app.db.models.user import User
from app.seeds.factories import (
    AmalCategoryFactory,
    AmalCompletionFactory,
    AmalFactory,
    AmalTemplateFactory,
    CountryFactory,
    HotelFactory,
    IconFactory,
    RestaurantFactory,
    RouteFactory,
    RouteImageFactory,
)
from app.seeds.seed.icon_amal import create_icons_amal
from app.services.auth.passwords import hash_password

SEED_MARKER_COUNTRY = "SEED__COUNTRY__"
SEED_MARKER_USER_EMAIL = "seed@seed.com"
SEED_MARKER_ICON = "SEED__ICON__"
SEED_MARKER_CATEGORY = "SEED__CATEGORY__"



async def purge_seeded(session: AsyncSession) -> None:
    seeded_user = await session.scalar(
        select(User).where(User.email == SEED_MARKER_USER_EMAIL)
    )
    if seeded_user:
        await session.execute(
            delete(AmalCompletion).where(AmalCompletion.userId == seeded_user.id)
        )
        await session.execute(delete(Amal).where(Amal.userId == seeded_user.id))

    await session.execute(
        delete(AmalCategory).where(AmalCategory.name.like(f"{SEED_MARKER_CATEGORY}%"))
    )
    await session.execute(delete(Icon).where(Icon.url.like(f"{SEED_MARKER_ICON}%")))

    seeded_countries = (
        await session.scalars(
            select(Country.id).where(Country.name.like(f"{SEED_MARKER_COUNTRY}%"))
        )
    ).all()

    if seeded_countries:
        await session.execute(
            delete(AmalTemplate).where(
                AmalTemplate.routeId.in_(
                    select(Route.id).where(Route.countryId.in_(seeded_countries))
                )
            )
        )
        await session.execute(
            delete(Restaurant).where(
                Restaurant.routeId.in_(
                    select(Route.id).where(Route.countryId.in_(seeded_countries))
                )
            )
        )
        await session.execute(
            delete(Hotel).where(
                Hotel.routeId.in_(
                    select(Route.id).where(Route.countryId.in_(seeded_countries))
                )
            )
        )
        await session.execute(
            delete(RouteImage).where(
                RouteImage.routeId.in_(
                    select(Route.id).where(Route.countryId.in_(seeded_countries))
                )
            )
        )
        await session.execute(
            delete(Route).where(Route.countryId.in_(seeded_countries))
        )
        await session.execute(delete(Country).where(Country.id.in_(seeded_countries)))

    await session.commit()


async def seed(session: AsyncSession) -> None:
    env = os.getenv("ENV", "dev")
    if env == "prod":
        raise RuntimeError("Seeding запрещен в prod окружении")

    await purge_seeded(session)
    await create_icons_amal(session)

    countries_count = 5
    routes_per_country = 8

    countries = []
    for i in range(countries_count):
        c = CountryFactory.build(
            name=f"{SEED_MARKER_COUNTRY}{i + 1} {random.choice(['Saudi Arabia', 'Turkey', 'UAE', 'Egypt', 'Jordan'])}"
        )
        session.add(c)
        countries.append(c)

    await session.flush()

    for country in countries:
        routes = []
        for _ in range(routes_per_country):
            r = RouteFactory.build(country=country)
            session.add(r)
            routes.append(r)

        await session.flush()

        for r in routes:
            for _ in range(random.randint(2, 6)):
                session.add(RouteImageFactory.build(route=r))

            for _ in range(random.randint(2, 8)):
                session.add(RestaurantFactory.build(route=r))

            for _ in range(random.randint(1, 5)):
                if random.random() < 0.2:
                    session.add(HotelFactory.build(route=r, location=None))
                else:
                    session.add(HotelFactory.build(route=r))

            for _ in range(random.randint(1, 4)):
                session.add(AmalTemplateFactory.build(route=r))

    await session.commit()
    await seed_amals(session)


async def seed_amals(session: AsyncSession) -> None:
    seed_user = await session.scalar(
        select(User).where(User.email == SEED_MARKER_USER_EMAIL)
    )
    if not seed_user:
        seed_user = User(
            email=SEED_MARKER_USER_EMAIL,
            password=hash_password("seedseed"),
            isVerified=True,
            isActive=True,
            name="Seed User",
        )
        session.add(seed_user)
        await session.flush()

    icons = []
    for i in range(5):
        icon = IconFactory.build(url=f"{SEED_MARKER_ICON}{i + 1}")
        session.add(icon)
        icons.append(icon)

    await session.flush()

    category_names = ["Намаз", "Дуа", "Зикр", "Чтение Корана", "Садака"]
    categories = []
    for name in category_names:
        cat = AmalCategoryFactory.build(name=f"{SEED_MARKER_CATEGORY}{name}")
        session.add(cat)
        categories.append(cat)

    await session.flush()

    amals = []
    for _ in range(random.randint(5, 10)):
        amal = AmalFactory.build(
            icon=random.choice(icons) if random.random() > 0.3 else None,
            category=random.choice(categories) if random.random() > 0.3 else None,
        )
        amal.userId = seed_user.id
        session.add(amal)
        amals.append(amal)

    await session.flush()

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

    await session.commit()


async def seed_db() -> None:
    async with AsyncSessionLocal() as session:
        await seed(session)
        print("Seed completed")


if __name__ == "__main__":
    asyncio.run(seed_db())
