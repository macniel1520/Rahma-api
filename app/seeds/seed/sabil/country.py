from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.country import Country
from app.seeds.factories import CountryFactory


async def create_country(
    session: AsyncSession,
    name: str,
    photo_url: Optional[str] = None,
) -> Country:
    """Create a country with the given name."""

    existing_country = await session.scalar(select(Country).where(Country.name == name))
    if existing_country:
        return existing_country

    country = CountryFactory.build(name=name)
    if photo_url:
        country.photoUrl = photo_url

    session.add(country)
    await session.commit()
    await session.refresh(country)
    return country


async def create_countries(
    session: AsyncSession,
    names: list[str],
) -> list[Country]:
    """Create multiple countries with the given names."""

    countries = []
    for name in names:
        country = await create_country(session, name)
        countries.append(country)

    return countries


async def create_countries_sabil(session: AsyncSession) -> list[Country]:
    """Create standard sabil countries."""
    countries_data = [
        (
            "Саудовская Аравия",
            "https://s3.geometria.ru/rahma-test/countries/saudi-arabia.webp",
        ),
        ("Иран", "https://s3.geometria.ru/rahma-test/countries/iran.jpg"),
        ("Ирак", "https://s3.geometria.ru/rahma-test/countries/iraq.jpg"),
        ("Египет", "https://s3.geometria.ru/rahma-test/countries/egypt.jpg"),
    ]

    countries = []
    for name, photo_url in countries_data:
        country = await create_country(session, name, photo_url)
        countries.append(country)

    return countries
