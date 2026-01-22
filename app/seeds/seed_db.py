import asyncio
import os
import random

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.engine import AsyncSessionLocal  # sessionmaker(...)
from app.db.models.amal_template import AmalTemplate
from app.db.models.country import Country
from app.db.models.hotel import Hotel
from app.db.models.restaurant import Restaurant
from app.db.models.route import Route
from app.db.models.route_image import RouteImage
from app.seeds.factories import (
    AmalTemplateFactory,
    CountryFactory,
    HotelFactory,
    RestaurantFactory,
    RouteFactory,
    RouteImageFactory,
)

SEED_MARKER_COUNTRY = "SEED__COUNTRY__"


async def purge_seeded(session: AsyncSession) -> None:
    seeded_countries = (
        await session.scalars(
            select(Country.id).where(Country.name.like(f"{SEED_MARKER_COUNTRY}%"))
        )
    ).all()

    if not seeded_countries:
        return

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
    await session.execute(delete(Route).where(Route.countryId.in_(seeded_countries)))
    await session.execute(delete(Country).where(Country.id.in_(seeded_countries)))

    await session.commit()


async def seed(session: AsyncSession) -> None:
    env = os.getenv("ENV", "dev")
    if env == "prod":
        raise RuntimeError("Seeding запрещен в prod окружении")

    await purge_seeded(session)

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


async def seed_db() -> None:
    async with AsyncSessionLocal() as session:
        await seed(session)
        print("Seed completed")


if __name__ == "__main__":
    asyncio.run(seed_db())
