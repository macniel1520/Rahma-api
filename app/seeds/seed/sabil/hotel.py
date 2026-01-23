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


HOTELS_DATA = [
    {
        "name": "Selat Al Bait Hotel",
        "description": "Из окон открывается вид на город. В распоряжении гостей отеля с 3 звездами — бесплатный Wi-Fi, доставка еды и напитков и круглосуточная стойка регистрации. К услугам гостей отеля — бесплатная частная парковка. Желающие осмотреть окрестности могут воспользоваться трансфером.",
        "photo_url": "https://s3.geometria.ru/rahma-test/hotels/selat-al-bait_hotel.webp",
        "avg_score": 4.8,
        "score_count": 12500,
        "avg_price": 450.0,
        "lat": "21.418890",
        "lng": "39.826180",
    },
    {
        "name": "Three Pearls Musalli Hotel",
        "description": "Отель в городе Мекка, находится в 1,9 км и 10 км от таких достопримечательностей, как Мечеть аль-Харам и Пещера Хира. Среди удобств отеля с 3 звездами — ресторан, а также номера с кондиционером, бесплатным Wi-Fi и собственной ванной комнатой. В распоряжении гостей доставка еды и напитков, услуги консьержа и камера хранения багажа.",
        "photo_url": "https://s3.geometria.ru/rahma-test/hotels/three_pearls_musali_hotel.webp",
        "avg_score": 4.6,
        "score_count": 8900,
        "avg_price": 320.0,
        "lat": "21.420100",
        "lng": "39.827500",
    },
    {
        "name": "Wirgan Hotel Al Nour",
        "description": "Отель с 4 звездами в городе Мекка, в 4 км и 7,7 км соответственно от таких достопримечательностей, как Пещера Хира и Мечеть аль-Харам. В числе прочих удобств — ресторан, детский клуб и доставка еды и напитков, а также бесплатный Wi-Fi на всей территории. На территории имеется частная парковка.",
        "photo_url": "https://s3.geometria.ru/rahma-test/hotels/wirgan_al_noor.webp",
        "avg_score": 4.5,
        "score_count": 6200,
        "avg_price": 280.0,
        "lat": "21.421500",
        "lng": "39.825900",
    },
]


async def create_hotels_sabil(
    session: AsyncSession,
    routes: list[Route],
) -> list[Hotel]:
    """Create standard sabil hotels for all routes."""
    
    all_hotels = []
    for route in routes:
        hotels = await create_hotels_for_route(session, route, HOTELS_DATA)
        all_hotels.extend(hotels)
    
    return all_hotels
