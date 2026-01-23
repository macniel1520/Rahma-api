from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.restaurant import Restaurant
from app.db.models.route import Route
from app.db.models.enums import CostLevel
from app.seeds.factories import RestaurantFactory


async def create_restaurant(
    session: AsyncSession,
    route: Route,
    name: str,
    description: Optional[str] = None,
    photo_url: Optional[str] = None,
    avg_score: Optional[float] = None,
    score_count: Optional[int] = None,
    is_haram: bool = False,
    cost_level: Optional[CostLevel] = None,
) -> Restaurant:
    """Create a restaurant with the given parameters."""
    
    existing_restaurant = await session.scalar(
        select(Restaurant).where(
            Restaurant.routeId == route.id,
            Restaurant.name == name
        )
    )
    if existing_restaurant:
        return existing_restaurant
    
    restaurant = RestaurantFactory.build(route=route)
    restaurant.name = name
    restaurant.isHaram = is_haram
    
    if description:
        restaurant.description = description
    if photo_url:
        restaurant.photoUrl = photo_url
    if avg_score is not None:
        restaurant.avgScore = avg_score
    if score_count is not None:
        restaurant.scoreCount = score_count
    if cost_level:
        restaurant.costLevel = cost_level
    
    session.add(restaurant)
    await session.commit()
    await session.refresh(restaurant)
    return restaurant


async def create_restaurants_for_route(
    session: AsyncSession,
    route: Route,
    restaurants_data: list[dict],
) -> list[Restaurant]:
    """Create multiple restaurants for a route."""
    
    restaurants = []
    for data in restaurants_data:
        restaurant = await create_restaurant(
            session,
            route=route,
            name=data["name"],
            description=data.get("description"),
            photo_url=data.get("photo_url"),
            avg_score=data.get("avg_score"),
            score_count=data.get("score_count"),
            is_haram=data.get("is_haram", False),
            cost_level=data.get("cost_level"),
        )
        restaurants.append(restaurant)
    
    return restaurants


RESTAURANTS_DATA = {
    "Мекка — священный город": [
        {
            "name": "Al Baik",
            "description": "Знаменитая сеть халяль фастфуда, популярная среди паломников.",
            "photo_url": "https://s3.geometria.ru/rahma-test/restaurants/al-baik.webp",
            "avg_score": 4.5,
            "score_count": 15000,
            "is_haram": False,
            "cost_level": CostLevel.LOW,
        },
        {
            "name": "Zamzam Restaurant",
            "description": "Ресторан традиционной арабской кухни рядом с Масджид аль-Харам.",
            "photo_url": "https://s3.geometria.ru/rahma-test/restaurants/zamzam.webp",
            "avg_score": 4.3,
            "score_count": 8500,
            "is_haram": False,
            "cost_level": CostLevel.MEDIUM,
        },
        {
            "name": "Hyatt Regency Restaurant",
            "description": "Ресторан при отеле с видом на Каабу.",
            "photo_url": "https://s3.geometria.ru/rahma-test/restaurants/hyatt-mecca.webp",
            "avg_score": 4.7,
            "score_count": 3200,
            "is_haram": False,
            "cost_level": CostLevel.HIGH,
        },
    ],
    "Медина — город Пророка": [
        {
            "name": "Tazaj",
            "description": "Сеть ресторанов с блюдами на гриле.",
            "photo_url": "https://s3.geometria.ru/rahma-test/restaurants/tazaj.webp",
            "avg_score": 4.2,
            "score_count": 6800,
            "is_haram": False,
            "cost_level": CostLevel.LOW,
        },
        {
            "name": "Madinah Dates Market",
            "description": "Рынок фиников с кафе и закусками.",
            "photo_url": "https://s3.geometria.ru/rahma-test/restaurants/dates-market.webp",
            "avg_score": 4.6,
            "score_count": 4500,
            "is_haram": False,
            "cost_level": CostLevel.LOW,
        },
    ],
    "Каир — город тысячи минаретов": [
        {
            "name": "Abou El Sid",
            "description": "Аутентичная египетская кухня в традиционном интерьере.",
            "photo_url": "https://s3.geometria.ru/rahma-test/restaurants/abou-el-sid.webp",
            "avg_score": 4.4,
            "score_count": 7200,
            "is_haram": False,
            "cost_level": CostLevel.MEDIUM,
        },
        {
            "name": "Felfela",
            "description": "Легендарный ресторан египетской кухни с 1959 года.",
            "photo_url": "https://s3.geometria.ru/rahma-test/restaurants/felfela.webp",
            "avg_score": 4.3,
            "score_count": 9100,
            "is_haram": False,
            "cost_level": CostLevel.LOW,
        },
    ],
}


async def create_restaurants_sabil(
    session: AsyncSession,
    routes: list[Route],
) -> list[Restaurant]:
    """Create standard sabil restaurants for given routes."""
    
    all_restaurants = []
    for route in routes:
        restaurants_data = RESTAURANTS_DATA.get(route.name, [])
        if restaurants_data:
            restaurants = await create_restaurants_for_route(session, route, restaurants_data)
            all_restaurants.extend(restaurants)
    
    return all_restaurants
