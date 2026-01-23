from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.route import Route
from app.db.models.country import Country
from app.db.models.enums import Category
from app.seeds.factories import RouteFactory


async def create_route(
    session: AsyncSession,
    name: str,
    country: Country,
    content: Optional[str] = None,
    photo_url: Optional[str] = None,
    category: Optional[Category] = None,
) -> Route:
    """Create a route with the given parameters."""
    
    existing_route = await session.scalar(
        select(Route).where(Route.name == name, Route.countryId == country.id)
    )
    if existing_route:
        return existing_route
    
    route = RouteFactory.build(country=country)
    route.name = name
    
    if content:
        route.content = content
    if photo_url:
        route.photoUrl = photo_url
    if category:
        route.category = category
    
    session.add(route)
    await session.commit()
    await session.refresh(route)
    return route


async def create_routes_for_country(
    session: AsyncSession,
    country: Country,
    routes_data: list[dict],
) -> list[Route]:
    """Create multiple routes for a country."""
    
    routes = []
    for data in routes_data:
        route = await create_route(
            session,
            name=data["name"],
            country=country,
            content=data.get("content"),
            photo_url=data.get("photo_url"),
            category=data.get("category"),
        )
        routes.append(route)
    
    return routes


ROUTES_DATA_SAUDI = [
    {
        "name": "Сафа и Марва",
        "content": "Холмы, между которыми совершается са‘й (обязательный обряд умры и хаджа).",
        "photo_url": "https://s3.geometria.ru/rahma-test/countries/saudi-arabia/as_safa_al_marva_mekka.webp",
        "category": Category.HAJJ,
    },
    {
        "name": "Масджид аль-Харам",
        "content": "Главная мечеть ислама. Кааба — направление молитвы (кибла) для всех мусульман. Макам Ибрахим, Колодец Замзам.",
        "photo_url": "https://s3.geometria.ru/rahma-test/countries/saudi-arabia/mechet_al_haram.webp",
        "category": Category.UMRAH,
    },
    {
        "name": "Мина (долина палаток)",
        "content": "Ритуал побивания шайтана (джамарат).",
        "photo_url": "https://s3.geometria.ru/rahma-test/countries/saudi-arabia/mina.webp",
        "category": Category.HISTORY,
    },
]

ROUTES_DATA_IRAN = [
    {
        "name": "Кум — мавзолей Фатимы Масумы",
        "content": "Главный религиозно-учебный центр шиитского мира. Часто посещается вместе с Мешхедом.",
        "photo_url": "https://s3.geometria.ru/rahma-test/countries/iran/mavzoley_fatimi_masume.webp",
        "category": Category.HISTORY,
    },
    {
        "name": "Мешхед — мавзолей имама Резы",
        "content": "Крупнейший религиозный комплекс в Иране и один из крупнейших в мире. Ежегодно десятки миллионов паломников из Ирана, Ирака, Азербайджана, Пакистана и др.",
        "photo_url": "https://s3.geometria.ru/rahma-test/countries/iran/mavzoley_imama_rezi.webp",
        "category": Category.UMRAH,
    },
    {
        "name": "Шираз — Шах-Черах",
        "content": "Шах-Черах — мавзолей Ахмада ибн Мусы, брата имама Резы. Известен зеркальной архитектурой и высокой религиозной значимостью.",
        "photo_url": "https://s3.geometria.ru/rahma-test/countries/iran/mavzoley_shah_cherah.webp",
        "category": Category.UMRAH,
    },
]

ROUTES_DATA_IRAQ = [
    {
        "name": "Кадимия (Багдад) — Аль-Кадимейн",
        "content": "Имам Муса аль-Казим (7-й) и Имам Мухаммад ат-Такый (9-й). Мавзолей Аль-Кадимейн. Постоянный поток паломников, особенно в религиозные даты.",
        "photo_url": "https://s3.geometria.ru/rahma-test/countries/iraq/al_kadhimiya_mosque.webp", 
        "category": Category.UMRAH,
    },
    {
        "name": "Кербела — мавзолей имама Хусейна",
        "content": "Харам имама Хусейна ибн Али (3-й шиитский имам). Рядом — мавзолей Аббаса ибн Али (часто воспринимаются как единый комплекс). Центральное место событий Ашуры и Арбаина.",
        "photo_url": "https://s3.geometria.ru/rahma-test/countries/iraq/kerbela.webp",
        "category": Category.HISTORY,
    },
    {
        "name": "Наджаф — мавзолей имама Али",
        "content": "Имам Муса аль-Казим (7-й) и Имам Мухаммад ат-Такый (9-й). Мавзолей Аль-Кадимейн. Постоянный поток паломников, особенно в религиозные даты.",
        "photo_url": "https://s3.geometria.ru/rahma-test/countries/iraq/mechet_imama_ali.webp",
        "category": Category.HISTORY,
    },
]

ROUTES_DATA_EGYPT = [
    {
        "name": "Каир — мечеть и университет Аль-Азхар",
        "content": "Главный религиозный центр суннитского ислама. Центр суннитского богословия и религиозного авторитета.",
        "photo_url": "https://s3.geometria.ru/rahma-test/countries/egypt/kair_al_azhar.webp",
        "category": Category.UMRAH,
    },
    {       
        "name": "Каир — мечеть Аль-Хусейна",
        "content": "Самая почитаемая шиитская святыня Египта. По преданию, здесь хранится голова имама Хусейна. Место паломничества шиитов и суннитов (в Египте распространено почитание Ахль аль-Бейт).",
        "photo_url": "https://s3.geometria.ru/rahma-test/countries/egypt/kair_mechet_al_husein.webp",
        "category": Category.HISTORY,
    },
    {       
        "name": "Каир — мечеть Сайида Зейнаб",
        "content": "Посвящена Зейнаб бинт Али, внучке пророка Мухаммада ﷺ. Один из главных центров суфийских маулидов (религиозных праздников).",
        "photo_url": "https://s3.geometria.ru/rahma-test/countries/egypt/mechet_sayeda_zainab_kair.webp",
        "category": Category.HISTORY,
    },

]


async def create_routes_sabil(
    session: AsyncSession,
    countries: list[Country],
) -> dict[str, list[Route]]:
    """Create standard sabil routes for given countries."""
    
    routes_map = {
        "Саудовская Аравия": ROUTES_DATA_SAUDI,
        "Иран": ROUTES_DATA_IRAN,
        "Ирак": ROUTES_DATA_IRAQ,
        "Египет": ROUTES_DATA_EGYPT,
    }
    
    result = {}
    for country in countries:
        routes_data = routes_map.get(country.name, [])
        if routes_data:
            routes = await create_routes_for_country(session, country, routes_data)
            result[country.name] = routes
    
    return result
