from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.amal_template import AmalTemplate
from app.db.models.route import Route
from app.db.models.enums import ReccuringRule
from app.seeds.factories import AmalTemplateFactory


async def create_amal_template(
    session: AsyncSession,
    route: Route,
    title: str,
    reccuring_rule: Optional[ReccuringRule] = None,
) -> AmalTemplate:
    """Create an amal template with the given parameters."""
    
    existing_template = await session.scalar(
        select(AmalTemplate).where(
            AmalTemplate.routeId == route.id,
            AmalTemplate.title == title
        )
    )
    if existing_template:
        return existing_template
    
    template = AmalTemplateFactory.build(route=route)
    template.title = title
    
    if reccuring_rule:
        template.reccuringRule = reccuring_rule
    
    session.add(template)
    await session.commit()
    await session.refresh(template)
    return template


async def create_amal_templates_for_route(
    session: AsyncSession,
    route: Route,
    templates_data: list[dict],
) -> list[AmalTemplate]:
    """Create multiple amal templates for a route."""
    
    templates = []
    for data in templates_data:
        template = await create_amal_template(
            session,
            route=route,
            title=data["title"],
            reccuring_rule=data.get("reccuring_rule"),
        )
        templates.append(template)
    
    return templates


AMAL_TEMPLATES_DATA = {
    "Мекка — священный город": [
        {"title": "Таваф вокруг Каабы", "reccuring_rule": ReccuringRule.ONCE},
        {"title": "Сай между Сафа и Марва", "reccuring_rule": ReccuringRule.ONCE},
        {"title": "Намаз у Макама Ибрахима", "reccuring_rule": ReccuringRule.ONCE},
        {"title": "Питьё воды Замзам", "reccuring_rule": ReccuringRule.DAILY},
        {"title": "Ночной намаз в Харам", "reccuring_rule": ReccuringRule.DAILY},
    ],
    "Медина — город Пророка": [
        {"title": "Намаз в мечети Пророка", "reccuring_rule": ReccuringRule.DAILY},
        {"title": "Посещение Равда", "reccuring_rule": ReccuringRule.ONCE},
        {"title": "Посещение кладбища Баки", "reccuring_rule": ReccuringRule.ONCE},
        {"title": "Намаз в мечети Куба", "reccuring_rule": ReccuringRule.WEEKLY},
    ],
    "Гора Арафат": [
        {"title": "Стояние на Арафате", "reccuring_rule": ReccuringRule.ONCE},
        {"title": "Дуа на горе Рахма", "reccuring_rule": ReccuringRule.ONCE},
    ],
    "Мина — долина палаток": [
        {"title": "Побивание камнями Джамарат", "reccuring_rule": ReccuringRule.ONCE},
        {"title": "Ночёвка в Мине", "reccuring_rule": ReccuringRule.ONCE},
    ],
    "Мешхед — город имама Резы": [
        {"title": "Зиярат святыни имама Резы", "reccuring_rule": ReccuringRule.ONCE},
        {"title": "Намаз в святыне", "reccuring_rule": ReccuringRule.DAILY},
    ],
    "Кербела — город имама Хусейна": [
        {"title": "Зиярат святыни имама Хусейна", "reccuring_rule": ReccuringRule.ONCE},
        {"title": "Зиярат святыни Аббаса", "reccuring_rule": ReccuringRule.ONCE},
    ],
    "Наджаф — город имама Али": [
        {"title": "Зиярат святыни имама Али", "reccuring_rule": ReccuringRule.ONCE},
        {"title": "Посещение кладбища Вади ас-Салам", "reccuring_rule": ReccuringRule.ONCE},
    ],
    "Каир — город тысячи минаретов": [
        {"title": "Намаз в мечети Аль-Хусейн", "reccuring_rule": ReccuringRule.ONCE},
        {"title": "Посещение мечети Аль-Азхар", "reccuring_rule": ReccuringRule.ONCE},
    ],
}


async def create_amal_templates_sabil(
    session: AsyncSession,
    routes: list[Route],
) -> list[AmalTemplate]:
    """Create standard sabil amal templates for given routes."""
    
    all_templates = []
    for route in routes:
        templates_data = AMAL_TEMPLATES_DATA.get(route.name, [])
        if templates_data:
            templates = await create_amal_templates_for_route(session, route, templates_data)
            all_templates.extend(templates)
    
    return all_templates
