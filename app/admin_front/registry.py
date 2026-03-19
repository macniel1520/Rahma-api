from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Awaitable, Callable
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.admin_front.schemas import (
    AmalCategoryCreate,
    AmalCategoryItem,
    CountryCreate,
    CountryItem,
    HotelCreate,
    HotelItem,
    IconCreate,
    IconItem,
    OptionItem,
    ResourceColumn,
    ResourceDescriptor,
    ResourceField,
    RouteImageCreate,
    RouteImageItem,
    RestaurantCreate,
    RestaurantItem,
    AmalTemplateCreate,
    AmalTemplateItem,
    RouteCreate,
    RouteItem,
)
from app.db.models.amal_category import AmalCategory
from app.db.models.country import Country
from app.db.models.enums import Category, CostLevel
from app.db.models.enums import ReccuringRule
from app.db.models.hotel import Hotel
from app.db.models.icon import Icon
from app.db.models.location import Location
from app.db.models.restaurant import Restaurant
from app.db.models.route import Route
from app.db.models.route_image import RouteImage
from app.db.models.amal_template import AmalTemplate


IMAGE_ACCEPT = ["image/jpeg", "image/png", "image/webp", "image/svg+xml", "image/jpg"]


@dataclass(frozen=True)
class ResourceDefinition:
    id: str
    label: str
    singular_label: str
    section: str
    entity_type: str
    create_label: str
    empty_state: str
    primary_field: str
    image_field: str | None
    description_field: str | None
    payload_model: type
    fields: list[ResourceField]
    columns: list[ResourceColumn]
    list_loader: Callable[[AsyncSession], Awaitable[list[dict[str, Any]]]]
    create_handler: Callable[[AsyncSession, Any], Awaitable[dict[str, Any]]]
    update_handler: Callable[[AsyncSession, UUID, Any], Awaitable[dict[str, Any]]]
    delete_handler: Callable[[AsyncSession, UUID], Awaitable[None]]
    options_loader: Callable[[AsyncSession], Awaitable[list[OptionItem]]] | None = None

    def descriptor(self) -> ResourceDescriptor:
        return ResourceDescriptor(
            id=self.id,
            label=self.label,
            singularLabel=self.singular_label,
            section=self.section,
            entityType=self.entity_type,
            createLabel=self.create_label,
            emptyState=self.empty_state,
            primaryField=self.primary_field,
            imageField=self.image_field,
            descriptionField=self.description_field,
            fields=self.fields,
            columns=self.columns,
        )


SECTIONS = [
    {"id": "dashboard", "label": "Обзор", "kind": "page"},
    {"id": "content", "label": "Контент", "kind": "group"},
    {"id": "actions", "label": "API методы", "kind": "page"},
]


def _dump(model) -> dict[str, Any]:
    return model.model_dump(by_alias=True)


async def load_country_options(session: AsyncSession) -> list[OptionItem]:
    rows = await session.scalars(select(Country).order_by(Country.name.asc()))
    return [OptionItem(value=str(item.id), label=item.name) for item in rows.all()]


async def load_route_options(session: AsyncSession) -> list[OptionItem]:
    rows = await session.scalars(select(Route).order_by(Route.name.asc()))
    return [OptionItem(value=str(item.id), label=item.name) for item in rows.all()]


async def list_countries(session: AsyncSession) -> list[dict[str, Any]]:
    routes_count_subq = (
        select(Route.countryId, func.count(Route.id).label("routes_count"))
        .group_by(Route.countryId)
        .subquery()
    )
    rows = await session.execute(
        select(Country, func.coalesce(routes_count_subq.c.routes_count, 0))
        .outerjoin(routes_count_subq, Country.id == routes_count_subq.c.countryId)
        .order_by(Country.createdAt.desc())
    )
    return [
        _dump(
            CountryItem(
                id=country.id,
                name=country.name,
                photoUrl=country.photoUrl,
                routes_count=routes_count,
            )
        )
        for country, routes_count in rows.all()
    ]


async def create_country(session: AsyncSession, payload: CountryCreate) -> dict[str, Any]:
    country = Country(name=payload.name.strip(), photoUrl=payload.photoUrl.strip())
    session.add(country)
    await session.flush()
    return _dump(
        CountryItem(
            id=country.id,
            name=country.name,
            photoUrl=country.photoUrl,
            routes_count=0,
        )
    )


async def update_country(session: AsyncSession, item_id: UUID, payload: CountryCreate) -> dict[str, Any]:
    country = await session.get(Country, item_id)
    if not country:
        raise KeyError("Country not found")

    country.name = payload.name.strip()
    country.photoUrl = payload.photoUrl.strip()
    await session.flush()
    routes_count = await session.scalar(select(func.count(Route.id)).where(Route.countryId == country.id)) or 0
    return _dump(
        CountryItem(
            id=country.id,
            name=country.name,
            photoUrl=country.photoUrl,
            routes_count=routes_count,
        )
    )


async def delete_country(session: AsyncSession, item_id: UUID) -> None:
    country = await session.get(Country, item_id)
    if not country:
        raise KeyError("Country not found")
    await session.delete(country)


async def list_routes(session: AsyncSession) -> list[dict[str, Any]]:
    hotel_count_subq = (
        select(Hotel.routeId, func.count(Hotel.id).label("hotel_count"))
        .group_by(Hotel.routeId)
        .subquery()
    )
    restaurant_count_subq = (
        select(Restaurant.routeId, func.count(Restaurant.id).label("restaurant_count"))
        .group_by(Restaurant.routeId)
        .subquery()
    )
    rows = await session.execute(
        select(
            Route,
            Country.name,
            func.coalesce(hotel_count_subq.c.hotel_count, 0),
            func.coalesce(restaurant_count_subq.c.restaurant_count, 0),
        )
        .join(Country, Country.id == Route.countryId)
        .outerjoin(hotel_count_subq, hotel_count_subq.c.routeId == Route.id)
        .outerjoin(restaurant_count_subq, restaurant_count_subq.c.routeId == Route.id)
        .order_by(Route.createdAt.desc())
    )
    return [
        _dump(
            RouteItem(
                id=route.id,
                name=route.name,
                content=route.content,
                photoUrl=route.photoUrl,
                views=route.views,
                category=route.category.value,
                countryId=route.countryId,
                country_name=country_name,
                hotels_count=hotel_count,
                restaurants_count=restaurant_count,
            )
        )
        for route, country_name, hotel_count, restaurant_count in rows.all()
    ]


async def create_route(session: AsyncSession, payload: RouteCreate) -> dict[str, Any]:
    route = Route(
        name=payload.name.strip(),
        content=payload.content.strip(),
        photoUrl=payload.photoUrl.strip(),
        views=payload.views,
        category=Category(payload.category),
        countryId=payload.countryId,
    )
    session.add(route)
    await session.flush()
    country_name = await session.scalar(select(Country.name).where(Country.id == route.countryId))
    return _dump(
        RouteItem(
            id=route.id,
            name=route.name,
            content=route.content,
            photoUrl=route.photoUrl,
            views=route.views,
            category=route.category.value,
            countryId=route.countryId,
            country_name=country_name or "",
            hotels_count=0,
            restaurants_count=0,
        )
    )


async def update_route(session: AsyncSession, item_id: UUID, payload: RouteCreate) -> dict[str, Any]:
    route = await session.get(Route, item_id)
    if not route:
        raise KeyError("Route not found")

    route.name = payload.name.strip()
    route.content = payload.content.strip()
    route.photoUrl = payload.photoUrl.strip()
    route.views = payload.views
    route.category = Category(payload.category)
    route.countryId = payload.countryId
    await session.flush()
    country_name = await session.scalar(select(Country.name).where(Country.id == route.countryId))
    hotel_count = await session.scalar(select(func.count(Hotel.id)).where(Hotel.routeId == route.id)) or 0
    restaurant_count = await session.scalar(select(func.count(Restaurant.id)).where(Restaurant.routeId == route.id)) or 0
    return _dump(
        RouteItem(
            id=route.id,
            name=route.name,
            content=route.content,
            photoUrl=route.photoUrl,
            views=route.views,
            category=route.category.value,
            countryId=route.countryId,
            country_name=country_name or "",
            hotels_count=hotel_count,
            restaurants_count=restaurant_count,
        )
    )


async def delete_route(session: AsyncSession, item_id: UUID) -> None:
    route = await session.get(Route, item_id)
    if not route:
        raise KeyError("Route not found")
    await session.delete(route)


async def list_hotels(session: AsyncSession) -> list[dict[str, Any]]:
    rows = await session.scalars(
        select(Hotel)
        .options(joinedload(Hotel.route), joinedload(Hotel.location))
        .order_by(Hotel.createdAt.desc())
    )
    return [
        _dump(
            HotelItem(
                id=hotel.id,
                name=hotel.name,
                description=hotel.description,
                photoUrl=hotel.photoUrl,
                avgScore=hotel.avgScore,
                scoreCount=hotel.scoreCount,
                avgPrice=hotel.avgPrice,
                routeId=hotel.routeId,
                route_name=hotel.route.name if hotel.route else "",
                locationId=hotel.locationId,
                lat=hotel.location.lat if hotel.location else None,
                lng=hotel.location.lng if hotel.location else None,
            )
        )
        for hotel in rows.unique().all()
    ]


async def create_hotel(session: AsyncSession, payload: HotelCreate) -> dict[str, Any]:
    location = Location(lat=str(payload.lat), lng=str(payload.lng))
    session.add(location)
    await session.flush()

    hotel = Hotel(
        name=payload.name.strip(),
        description=payload.description.strip(),
        photoUrl=payload.photoUrl.strip(),
        avgScore=payload.avgScore,
        scoreCount=payload.scoreCount,
        avgPrice=payload.avgPrice,
        routeId=payload.routeId,
        locationId=location.id,
    )
    session.add(hotel)
    await session.flush()
    route_name = await session.scalar(select(Route.name).where(Route.id == hotel.routeId))
    return _dump(
        HotelItem(
            id=hotel.id,
            name=hotel.name,
            description=hotel.description,
            photoUrl=hotel.photoUrl,
            avgScore=hotel.avgScore,
            scoreCount=hotel.scoreCount,
            avgPrice=hotel.avgPrice,
            routeId=hotel.routeId,
            route_name=route_name or "",
            locationId=location.id,
            lat=location.lat,
            lng=location.lng,
        )
    )


async def update_hotel(session: AsyncSession, item_id: UUID, payload: HotelCreate) -> dict[str, Any]:
    hotel = await session.get(Hotel, item_id)
    if not hotel:
        raise KeyError("Hotel not found")

    location = await session.get(Location, hotel.locationId) if hotel.locationId else None
    if location is None:
        location = Location(lat=str(payload.lat), lng=str(payload.lng))
        session.add(location)
        await session.flush()
        hotel.locationId = location.id
    else:
        location.lat = str(payload.lat)
        location.lng = str(payload.lng)

    hotel.name = payload.name.strip()
    hotel.description = payload.description.strip()
    hotel.photoUrl = payload.photoUrl.strip()
    hotel.avgScore = payload.avgScore
    hotel.scoreCount = payload.scoreCount
    hotel.avgPrice = payload.avgPrice
    hotel.routeId = payload.routeId
    await session.flush()
    route_name = await session.scalar(select(Route.name).where(Route.id == hotel.routeId))
    return _dump(
        HotelItem(
            id=hotel.id,
            name=hotel.name,
            description=hotel.description,
            photoUrl=hotel.photoUrl,
            avgScore=hotel.avgScore,
            scoreCount=hotel.scoreCount,
            avgPrice=hotel.avgPrice,
            routeId=hotel.routeId,
            route_name=route_name or "",
            locationId=hotel.locationId,
            lat=location.lat if location else None,
            lng=location.lng if location else None,
        )
    )


async def delete_hotel(session: AsyncSession, item_id: UUID) -> None:
    hotel = await session.get(Hotel, item_id)
    if not hotel:
        raise KeyError("Hotel not found")
    location_id = hotel.locationId
    await session.delete(hotel)
    if location_id:
        location = await session.get(Location, location_id)
        if location:
            await session.delete(location)


async def list_restaurants(session: AsyncSession) -> list[dict[str, Any]]:
    rows = await session.scalars(
        select(Restaurant)
        .options(joinedload(Restaurant.route))
        .order_by(Restaurant.createdAt.desc())
    )
    return [
        _dump(
            RestaurantItem(
                id=restaurant.id,
                name=restaurant.name,
                description=restaurant.description,
                photoUrl=restaurant.photoUrl,
                avgScore=restaurant.avgScore,
                scoreCount=restaurant.scoreCount,
                isHaram=restaurant.isHaram,
                costLevel=restaurant.costLevel.value,
                routeId=restaurant.routeId,
                route_name=restaurant.route.name if restaurant.route else "",
            )
        )
        for restaurant in rows.unique().all()
    ]


async def create_restaurant(session: AsyncSession, payload: RestaurantCreate) -> dict[str, Any]:
    restaurant = Restaurant(
        name=payload.name.strip(),
        description=payload.description.strip(),
        photoUrl=payload.photoUrl.strip(),
        avgScore=payload.avgScore,
        scoreCount=payload.scoreCount,
        isHaram=payload.isHaram,
        costLevel=CostLevel(payload.costLevel),
        routeId=payload.routeId,
    )
    session.add(restaurant)
    await session.flush()
    route_name = await session.scalar(select(Route.name).where(Route.id == restaurant.routeId))
    return _dump(
        RestaurantItem(
            id=restaurant.id,
            name=restaurant.name,
            description=restaurant.description,
            photoUrl=restaurant.photoUrl,
            avgScore=restaurant.avgScore,
            scoreCount=restaurant.scoreCount,
            isHaram=restaurant.isHaram,
            costLevel=restaurant.costLevel.value,
            routeId=restaurant.routeId,
            route_name=route_name or "",
        )
    )


async def update_restaurant(session: AsyncSession, item_id: UUID, payload: RestaurantCreate) -> dict[str, Any]:
    restaurant = await session.get(Restaurant, item_id)
    if not restaurant:
        raise KeyError("Restaurant not found")

    restaurant.name = payload.name.strip()
    restaurant.description = payload.description.strip()
    restaurant.photoUrl = payload.photoUrl.strip()
    restaurant.avgScore = payload.avgScore
    restaurant.scoreCount = payload.scoreCount
    restaurant.isHaram = payload.isHaram
    restaurant.costLevel = CostLevel(payload.costLevel)
    restaurant.routeId = payload.routeId
    await session.flush()
    route_name = await session.scalar(select(Route.name).where(Route.id == restaurant.routeId))
    return _dump(
        RestaurantItem(
            id=restaurant.id,
            name=restaurant.name,
            description=restaurant.description,
            photoUrl=restaurant.photoUrl,
            avgScore=restaurant.avgScore,
            scoreCount=restaurant.scoreCount,
            isHaram=restaurant.isHaram,
            costLevel=restaurant.costLevel.value,
            routeId=restaurant.routeId,
            route_name=route_name or "",
        )
    )


async def delete_restaurant(session: AsyncSession, item_id: UUID) -> None:
    restaurant = await session.get(Restaurant, item_id)
    if not restaurant:
        raise KeyError("Restaurant not found")
    await session.delete(restaurant)


async def list_route_images(session: AsyncSession) -> list[dict[str, Any]]:
    rows = await session.scalars(
        select(RouteImage)
        .options(joinedload(RouteImage.route))
        .order_by(RouteImage.createdAt.desc())
    )
    return [
        _dump(
            RouteImageItem(
                id=image.id,
                url=image.url,
                routeId=image.routeId,
                route_name=image.route.name if image.route else "",
            )
        )
        for image in rows.unique().all()
    ]


async def create_route_image(session: AsyncSession, payload: RouteImageCreate) -> dict[str, Any]:
    image = RouteImage(
        url=payload.url.strip(),
        routeId=payload.routeId,
    )
    session.add(image)
    await session.flush()
    route_name = await session.scalar(select(Route.name).where(Route.id == image.routeId))
    return _dump(
        RouteImageItem(
            id=image.id,
            url=image.url,
            routeId=image.routeId,
            route_name=route_name or "",
        )
    )


async def update_route_image(session: AsyncSession, item_id: UUID, payload: RouteImageCreate) -> dict[str, Any]:
    image = await session.get(RouteImage, item_id)
    if not image:
        raise KeyError("Route image not found")

    image.url = payload.url.strip()
    image.routeId = payload.routeId
    await session.flush()
    route_name = await session.scalar(select(Route.name).where(Route.id == image.routeId))
    return _dump(
        RouteImageItem(
            id=image.id,
            url=image.url,
            routeId=image.routeId,
            route_name=route_name or "",
        )
    )


async def delete_route_image(session: AsyncSession, item_id: UUID) -> None:
    image = await session.get(RouteImage, item_id)
    if not image:
        raise KeyError("Route image not found")
    await session.delete(image)


async def list_icons(session: AsyncSession) -> list[dict[str, Any]]:
    rows = await session.scalars(select(Icon).order_by(Icon.createdAt.desc()))
    return [_dump(IconItem(id=icon.id, url=icon.url)) for icon in rows.all()]


async def create_icon(session: AsyncSession, payload: IconCreate) -> dict[str, Any]:
    icon = Icon(url=payload.url.strip())
    session.add(icon)
    await session.flush()
    return _dump(IconItem(id=icon.id, url=icon.url))


async def update_icon(session: AsyncSession, item_id: UUID, payload: IconCreate) -> dict[str, Any]:
    icon = await session.get(Icon, item_id)
    if not icon:
        raise KeyError("Icon not found")

    icon.url = payload.url.strip()
    await session.flush()
    return _dump(IconItem(id=icon.id, url=icon.url))


async def delete_icon(session: AsyncSession, item_id: UUID) -> None:
    icon = await session.get(Icon, item_id)
    if not icon:
        raise KeyError("Icon not found")
    await session.delete(icon)


async def list_amal_categories(session: AsyncSession) -> list[dict[str, Any]]:
    rows = await session.scalars(select(AmalCategory).order_by(AmalCategory.createdAt.desc()))
    return [_dump(AmalCategoryItem(id=item.id, name=item.name)) for item in rows.all()]


async def create_amal_category(session: AsyncSession, payload: AmalCategoryCreate) -> dict[str, Any]:
    category = AmalCategory(name=payload.name.strip())
    session.add(category)
    await session.flush()
    return _dump(AmalCategoryItem(id=category.id, name=category.name))


async def update_amal_category(
    session: AsyncSession,
    item_id: UUID,
    payload: AmalCategoryCreate,
) -> dict[str, Any]:
    category = await session.get(AmalCategory, item_id)
    if not category:
        raise KeyError("Amal category not found")

    category.name = payload.name.strip()
    await session.flush()
    return _dump(AmalCategoryItem(id=category.id, name=category.name))


async def delete_amal_category(session: AsyncSession, item_id: UUID) -> None:
    category = await session.get(AmalCategory, item_id)
    if not category:
        raise KeyError("Amal category not found")
    await session.delete(category)


async def list_amal_templates(session: AsyncSession) -> list[dict[str, Any]]:
    rows = await session.scalars(
        select(AmalTemplate)
        .options(joinedload(AmalTemplate.route))
        .order_by(AmalTemplate.createdAt.desc())
    )
    return [
        _dump(
            AmalTemplateItem(
                id=item.id,
                title=item.title,
                reccuringRule=item.reccuringRule.value,
                routeId=item.routeId,
                route_name=item.route.name if item.route else "",
            )
        )
        for item in rows.unique().all()
    ]


async def create_amal_template(session: AsyncSession, payload: AmalTemplateCreate) -> dict[str, Any]:
    template = AmalTemplate(
        title=payload.title.strip(),
        reccuringRule=ReccuringRule(payload.reccuringRule),
        routeId=payload.routeId,
    )
    session.add(template)
    await session.flush()
    route_name = await session.scalar(select(Route.name).where(Route.id == template.routeId))
    return _dump(
        AmalTemplateItem(
            id=template.id,
            title=template.title,
            reccuringRule=template.reccuringRule.value,
            routeId=template.routeId,
            route_name=route_name or "",
        )
    )


async def update_amal_template(
    session: AsyncSession,
    item_id: UUID,
    payload: AmalTemplateCreate,
) -> dict[str, Any]:
    template = await session.get(AmalTemplate, item_id)
    if not template:
        raise KeyError("Amal template not found")

    template.title = payload.title.strip()
    template.reccuringRule = ReccuringRule(payload.reccuringRule)
    template.routeId = payload.routeId
    await session.flush()
    route_name = await session.scalar(select(Route.name).where(Route.id == template.routeId))
    return _dump(
        AmalTemplateItem(
            id=template.id,
            title=template.title,
            reccuringRule=template.reccuringRule.value,
            routeId=template.routeId,
            route_name=route_name or "",
        )
    )


async def delete_amal_template(session: AsyncSession, item_id: UUID) -> None:
    template = await session.get(AmalTemplate, item_id)
    if not template:
        raise KeyError("Amal template not found")
    await session.delete(template)


RESOURCE_DEFINITIONS: dict[str, ResourceDefinition] = {
    "countries": ResourceDefinition(
        id="countries",
        label="Страны",
        singular_label="Страна",
        section="content",
        entity_type="country",
        create_label="Добавить страну",
        empty_state="Пока нет ни одной страны.",
        primary_field="name",
        image_field="photoUrl",
        description_field=None,
        payload_model=CountryCreate,
        fields=[
            ResourceField(name="name", label="Название", type="text", required=True),
            ResourceField(
                name="photoUpload",
                label="Фото",
                type="upload",
                required=True,
                bind="photoUrl",
                accept=IMAGE_ACCEPT,
                helpText="Изображение сразу загружается в S3 и записывает ссылку в photoUrl.",
            ),
        ],
        columns=[
            ResourceColumn(key="routes_count", label="Маршрутов", kind="number"),
            ResourceColumn(key="photoUrl", label="Фото", kind="image"),
        ],
        list_loader=list_countries,
        create_handler=create_country,
        update_handler=update_country,
        delete_handler=delete_country,
        options_loader=load_country_options,
    ),
    "routes": ResourceDefinition(
        id="routes",
        label="Маршруты",
        singular_label="Маршрут",
        section="content",
        entity_type="route",
        create_label="Добавить маршрут",
        empty_state="Пока нет ни одного маршрута.",
        primary_field="name",
        image_field="photoUrl",
        description_field="content",
        payload_model=RouteCreate,
        fields=[
            ResourceField(name="name", label="Название", type="text", required=True),
            ResourceField(name="content", label="Описание", type="textarea", required=True),
            ResourceField(
                name="category",
                label="Категория",
                type="select",
                required=True,
                options=[
                    OptionItem(value="hajj", label="Hajj"),
                    OptionItem(value="umrah", label="Umrah"),
                    OptionItem(value="history", label="History"),
                ],
            ),
            ResourceField(
                name="countryId",
                label="Страна",
                type="select",
                required=True,
                optionsResource="countries",
            ),
            ResourceField(
                name="photoUpload",
                label="Фото",
                type="upload",
                required=True,
                bind="photoUrl",
                accept=IMAGE_ACCEPT,
            ),
            ResourceField(name="views", label="Просмотры", type="number", default=0, min=0, step=1),
        ],
        columns=[
            ResourceColumn(key="country_name", label="Страна"),
            ResourceColumn(key="category", label="Категория"),
            ResourceColumn(key="views", label="Просмотры", kind="number"),
            ResourceColumn(key="hotels_count", label="Отелей", kind="number"),
            ResourceColumn(key="restaurants_count", label="Ресторанов", kind="number"),
        ],
        list_loader=list_routes,
        create_handler=create_route,
        update_handler=update_route,
        delete_handler=delete_route,
        options_loader=load_route_options,
    ),
    "hotels": ResourceDefinition(
        id="hotels",
        label="Отели",
        singular_label="Отель",
        section="content",
        entity_type="hotel",
        create_label="Добавить отель",
        empty_state="Пока нет ни одного отеля.",
        primary_field="name",
        image_field="photoUrl",
        description_field="description",
        payload_model=HotelCreate,
        fields=[
            ResourceField(name="name", label="Название", type="text", required=True),
            ResourceField(name="description", label="Описание", type="textarea", required=True),
            ResourceField(
                name="photoUpload",
                label="Фото",
                type="upload",
                required=True,
                bind="photoUrl",
                accept=IMAGE_ACCEPT,
            ),
            ResourceField(name="avgScore", label="Рейтинг", type="number", required=True, min=0, max=5, step=0.1),
            ResourceField(name="scoreCount", label="Количество оценок", type="number", required=True, min=0, step=1),
            ResourceField(name="avgPrice", label="Средняя цена", type="number", required=True, min=0, step=0.1),
            ResourceField(
                name="routeId",
                label="Маршрут",
                type="select",
                required=True,
                optionsResource="routes",
            ),
            ResourceField(name="lat", label="Широта", type="number", required=True, step=0.000001),
            ResourceField(name="lng", label="Долгота", type="number", required=True, step=0.000001),
        ],
        columns=[
            ResourceColumn(key="route_name", label="Маршрут"),
            ResourceColumn(key="avgScore", label="Рейтинг", kind="number"),
            ResourceColumn(key="avgPrice", label="Цена", kind="number"),
            ResourceColumn(key="photoUrl", label="Фото", kind="image"),
        ],
        list_loader=list_hotels,
        create_handler=create_hotel,
        update_handler=update_hotel,
        delete_handler=delete_hotel,
    ),
    "restaurants": ResourceDefinition(
        id="restaurants",
        label="Рестораны",
        singular_label="Ресторан",
        section="content",
        entity_type="restaurant",
        create_label="Добавить ресторан",
        empty_state="Пока нет ни одного ресторана.",
        primary_field="name",
        image_field="photoUrl",
        description_field="description",
        payload_model=RestaurantCreate,
        fields=[
            ResourceField(name="name", label="Название", type="text", required=True),
            ResourceField(name="description", label="Описание", type="textarea", required=True),
            ResourceField(
                name="photoUpload",
                label="Фото",
                type="upload",
                required=True,
                bind="photoUrl",
                accept=IMAGE_ACCEPT,
            ),
            ResourceField(name="avgScore", label="Рейтинг", type="number", required=True, min=0, max=5, step=0.1),
            ResourceField(name="scoreCount", label="Количество оценок", type="number", required=True, min=0, step=1),
            ResourceField(
                name="costLevel",
                label="Уровень цены",
                type="select",
                required=True,
                options=[
                    OptionItem(value="low", label="Low"),
                    OptionItem(value="medium", label="Medium"),
                    OptionItem(value="high", label="High"),
                ],
            ),
            ResourceField(name="isHaram", label="Харам", type="boolean"),
            ResourceField(
                name="routeId",
                label="Маршрут",
                type="select",
                required=True,
                optionsResource="routes",
            ),
        ],
        columns=[
            ResourceColumn(key="route_name", label="Маршрут"),
            ResourceColumn(key="avgScore", label="Рейтинг", kind="number"),
            ResourceColumn(key="costLevel", label="Уровень цены"),
            ResourceColumn(key="isHaram", label="Харам", kind="boolean"),
            ResourceColumn(key="photoUrl", label="Фото", kind="image"),
        ],
        list_loader=list_restaurants,
        create_handler=create_restaurant,
        update_handler=update_restaurant,
        delete_handler=delete_restaurant,
    ),
    "route-images": ResourceDefinition(
        id="route-images",
        label="Картинки маршрутов",
        singular_label="Картинка маршрута",
        section="content",
        entity_type="route",
        create_label="Добавить картинку маршрута",
        empty_state="Пока нет ни одной картинки маршрута.",
        primary_field="url",
        image_field="url",
        description_field=None,
        payload_model=RouteImageCreate,
        fields=[
            ResourceField(
                name="routeId",
                label="Маршрут",
                type="select",
                required=True,
                optionsResource="routes",
            ),
            ResourceField(
                name="routeImageUpload",
                label="Изображение маршрута",
                type="upload",
                required=True,
                bind="url",
                accept=IMAGE_ACCEPT,
            ),
        ],
        columns=[
            ResourceColumn(key="route_name", label="Маршрут"),
            ResourceColumn(key="url", label="Изображение", kind="image"),
        ],
        list_loader=list_route_images,
        create_handler=create_route_image,
        update_handler=update_route_image,
        delete_handler=delete_route_image,
    ),
    "icons": ResourceDefinition(
        id="icons",
        label="Иконки",
        singular_label="Иконка",
        section="content",
        entity_type="icon",
        create_label="Добавить иконку",
        empty_state="Пока нет ни одной иконки.",
        primary_field="url",
        image_field="url",
        description_field=None,
        payload_model=IconCreate,
        fields=[
            ResourceField(
                name="iconUpload",
                label="Иконка",
                type="upload",
                required=True,
                bind="url",
                accept=IMAGE_ACCEPT,
                helpText="Для иконок можно использовать png, webp или svg, если клиент умеет их рендерить.",
            ),
        ],
        columns=[ResourceColumn(key="url", label="Иконка", kind="image")],
        list_loader=list_icons,
        create_handler=create_icon,
        update_handler=update_icon,
        delete_handler=delete_icon,
    ),
    "amal-categories": ResourceDefinition(
        id="amal-categories",
        label="Категории амалей",
        singular_label="Категория амаля",
        section="content",
        entity_type="amal-category",
        create_label="Добавить категорию амаля",
        empty_state="Пока нет ни одной категории амалей.",
        primary_field="name",
        image_field=None,
        description_field=None,
        payload_model=AmalCategoryCreate,
        fields=[ResourceField(name="name", label="Название", type="text", required=True)],
        columns=[ResourceColumn(key="name", label="Название")],
        list_loader=list_amal_categories,
        create_handler=create_amal_category,
        update_handler=update_amal_category,
        delete_handler=delete_amal_category,
    ),
    "amal-templates": ResourceDefinition(
        id="amal-templates",
        label="Шаблоны амалей",
        singular_label="Шаблон амаля",
        section="content",
        entity_type="amal-template",
        create_label="Добавить шаблон амаля",
        empty_state="Пока нет ни одного шаблона амалей.",
        primary_field="title",
        image_field=None,
        description_field=None,
        payload_model=AmalTemplateCreate,
        fields=[
            ResourceField(name="title", label="Название", type="text", required=True),
            ResourceField(
                name="reccuringRule",
                label="Повторение",
                type="select",
                required=True,
                options=[
                    OptionItem(value="once", label="Один раз"),
                    OptionItem(value="daily", label="Каждый день"),
                    OptionItem(value="weekly", label="Каждую неделю"),
                    OptionItem(value="monthly", label="Каждый месяц"),
                    OptionItem(value="yearly", label="Каждый год"),
                ],
            ),
            ResourceField(
                name="routeId",
                label="Маршрут",
                type="select",
                required=True,
                optionsResource="routes",
            ),
        ],
        columns=[
            ResourceColumn(key="route_name", label="Маршрут"),
            ResourceColumn(key="reccuringRule", label="Повторение"),
        ],
        list_loader=list_amal_templates,
        create_handler=create_amal_template,
        update_handler=update_amal_template,
        delete_handler=delete_amal_template,
    ),
}


def get_resource_definition(resource_id: str) -> ResourceDefinition | None:
    return RESOURCE_DEFINITIONS.get(resource_id)


def list_resource_descriptors() -> list[ResourceDescriptor]:
    return [definition.descriptor() for definition in RESOURCE_DEFINITIONS.values()]
