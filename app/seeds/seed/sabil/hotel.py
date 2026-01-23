from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.hotel import Hotel
from app.db.models.route import Route
from app.db.models.location import Location
from app.seeds.factories import HotelFactory
from app.seeds.seed.sabil.location_hotel import create_location_optional


async def create_hotel(
    session: AsyncSession,
    route: Route,
    name: str,
    description: Optional[str] = None,
    photo_url: Optional[str] = None,
    avg_score: Optional[float] = None,
    score_count: Optional[int] = None,
    avg_price: Optional[float] = None,
    lat: Optional[str] = None,
    lng: Optional[str] = None,
) -> Hotel:
    """Create a hotel with the given parameters."""
    
    existing_hotel = await session.scalar(
        select(Hotel).where(
            Hotel.routeId == route.id,
            Hotel.name == name
        )
    )
    if existing_hotel:
        return existing_hotel
    
    location = await create_location_optional(session, lat, lng)
    
    hotel = HotelFactory.build(route=route, location=location)
    hotel.name = name
    
    if description:
        hotel.description = description
    if photo_url:
        hotel.photoUrl = photo_url
    if avg_score is not None:
        hotel.avgScore = avg_score
    if score_count is not None:
        hotel.scoreCount = score_count
    if avg_price is not None:
        hotel.avgPrice = avg_price
    
    session.add(hotel)
    await session.commit()
    await session.refresh(hotel)
    return hotel


async def create_hotels_for_route(
    session: AsyncSession,
    route: Route,
    hotels_data: list[dict],
) -> list[Hotel]:
    """Create multiple hotels for a route."""
    
    hotels = []
    for data in hotels_data:
        hotel = await create_hotel(
            session,
            route=route,
            name=data["name"],
            description=data.get("description"),
            photo_url=data.get("photo_url"),
            avg_score=data.get("avg_score"),
            score_count=data.get("score_count"),
            avg_price=data.get("avg_price"),
            lat=data.get("lat"),
            lng=data.get("lng"),
        )
        hotels.append(hotel)
    
    return hotels


HOTELS_DATA = {
    "Мекка — священный город": [
        {
            "name": "Makkah Clock Royal Tower",
            "description": "Роскошный отель с видом на Каабу в комплексе Абрадж аль-Бейт.",
            "photo_url": "https://s3.geometria.ru/rahma-test/hotels/clock-tower.webp",
            "avg_score": 4.8,
            "score_count": 12500,
            "avg_price": 450.0,
            "lat": "21.418890",
            "lng": "39.826180",
        },
        {
            "name": "Swissotel Makkah",
            "description": "5-звёздочный отель в нескольких минутах ходьбы от Масджид аль-Харам.",
            "photo_url": "https://s3.geometria.ru/rahma-test/hotels/swissotel-makkah.webp",
            "avg_score": 4.6,
            "score_count": 8900,
            "avg_price": 320.0,
            "lat": "21.420100",
            "lng": "39.827500",
        },
        {
            "name": "Hilton Suites Makkah",
            "description": "Комфортабельные номера-люкс для семей и групп паломников.",
            "photo_url": "https://s3.geometria.ru/rahma-test/hotels/hilton-makkah.webp",
            "avg_score": 4.5,
            "score_count": 6200,
            "avg_price": 280.0,
            "lat": "21.421500",
            "lng": "39.825900",
        },
    ],
    "Медина — город Пророка": [
        {
            "name": "The Oberoi Madina",
            "description": "Элегантный отель рядом с мечетью Пророка.",
            "photo_url": "https://s3.geometria.ru/rahma-test/hotels/oberoi-madina.webp",
            "avg_score": 4.9,
            "score_count": 5600,
            "avg_price": 380.0,
            "lat": "24.467700",
            "lng": "39.610500",
        },
        {
            "name": "Dar Al Taqwa Hotel",
            "description": "Отель с прямым выходом к площади мечети Пророка.",
            "photo_url": "https://s3.geometria.ru/rahma-test/hotels/dar-al-taqwa.webp",
            "avg_score": 4.4,
            "score_count": 7800,
            "avg_price": 220.0,
            "lat": "24.468200",
            "lng": "39.611000",
        },
    ],
    "Каир — город тысячи минаретов": [
        {
            "name": "Four Seasons Cairo at Nile Plaza",
            "description": "Роскошный отель на берегу Нила с видом на пирамиды.",
            "photo_url": "https://s3.geometria.ru/rahma-test/hotels/four-seasons-cairo.webp",
            "avg_score": 4.7,
            "score_count": 4300,
            "avg_price": 350.0,
            "lat": "30.044500",
            "lng": "31.232800",
        },
        {
            "name": "Marriott Mena House",
            "description": "Исторический отель у подножия пирамид Гизы.",
            "photo_url": "https://s3.geometria.ru/rahma-test/hotels/mena-house.webp",
            "avg_score": 4.6,
            "score_count": 5100,
            "avg_price": 280.0,
            "lat": "29.976400",
            "lng": "31.138100",
        },
    ],
    "Мешхед — город имама Резы": [
        {
            "name": "Darvishi Royal Hotel",
            "description": "5-звёздочный отель недалеко от святыни имама Резы.",
            "photo_url": "https://s3.geometria.ru/rahma-test/hotels/darvishi.webp",
            "avg_score": 4.5,
            "score_count": 3200,
            "avg_price": 150.0,
            "lat": "36.287600",
            "lng": "59.615800",
        },
    ],
    "Кербела — город имама Хусейна": [
        {
            "name": "Karbala Hotel",
            "description": "Отель рядом со святыней имама Хусейна.",
            "photo_url": "https://s3.geometria.ru/rahma-test/hotels/karbala-hotel.webp",
            "avg_score": 4.2,
            "score_count": 2100,
            "avg_price": 80.0,
            "lat": "32.616700",
            "lng": "44.032200",
        },
    ],
}


async def create_hotels_sabil(
    session: AsyncSession,
    routes: list[Route],
) -> list[Hotel]:
    """Create standard sabil hotels for given routes."""
    
    all_hotels = []
    for route in routes:
        hotels_data = HOTELS_DATA.get(route.name, [])
        if hotels_data:
            hotels = await create_hotels_for_route(session, route, hotels_data)
            all_hotels.extend(hotels)
    
    return all_hotels
