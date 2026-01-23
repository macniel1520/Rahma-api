from typing import List, Optional
from uuid import UUID

from langchain_core.tools import tool

from app.api.v1.schemas.sabil.amal_template_schema import AmalTemplateRead
from app.api.v1.schemas.sabil.hotel_schema import HotelRead
from app.api.v1.schemas.sabil.restaurant_schema import RestaurantRead
from app.db.cruds.route_search_repository import RouteSearchRepository


class SearchTools:
    """Инструменты для поиска данных о маршрутах, отелях, ресторанах и шаблонах амалов"""

    def __init__(self, route_search_repo: RouteSearchRepository):
        self._route_search_repo = route_search_repo

    @tool("search_hotels")
    async def search_hotels(self, route_id: str, limit: int = 3) -> List[HotelRead]:
        """
        Поиск отелей по маршруту. Используйте этот инструмент когда пользователь спрашивает о жилье или отелях.

        Args:
            route_id: UUID маршрута
            limit: Максимальное количество отелей для возврата (по умолчанию 3)

        Returns:
            Список лучших отелей по рейтингу
        """
        try:
            route_uuid = UUID(route_id)
            hotels = await self._route_search_repo.search_hotels_by_route(
                route_id=route_uuid, limit=limit
            )
            return [HotelRead.model_validate(hotel) for hotel in hotels]
        except ValueError:
            return []

    @tool("search_restaurants")
    async def search_restaurants(
        self, route_id: str, limit: int = 3
    ) -> List[RestaurantRead]:
        """
        Поиск ресторанов по маршруту. Используйте этот инструмент когда пользователь спрашивает о еде или ресторанах.

        Args:
            route_id: UUID маршрута
            limit: Максимальное количество ресторанов для возврата (по умолчанию 3)

        Returns:
            Список лучших ресторанов по рейтингу
        """
        try:
            route_uuid = UUID(route_id)
            restaurants = await self._route_search_repo.search_restaurants_by_route(
                route_id=route_uuid, limit=limit
            )
            return [
                RestaurantRead.model_validate(restaurant) for restaurant in restaurants
            ]
        except ValueError:
            return []

    @tool("search_amal_templates")
    async def search_amal_templates(
        self, route_id: str, limit: int = 3
    ) -> List[AmalTemplateRead]:
        """
        Поиск шаблонов амалов по маршруту. Используйте этот инструмент когда пользователь спрашивает о молитвах, намазе или амалах.

        Args:
            route_id: UUID маршрута
            limit: Максимальное количество шаблонов для возврата (по умолчанию 3)

        Returns:
            Список шаблонов амалов
        """
        try:
            route_uuid = UUID(route_id)
            templates = await self._route_search_repo.search_amal_templates_by_route(
                route_id=route_uuid, limit=limit
            )
            return [AmalTemplateRead.model_validate(template) for template in templates]
        except ValueError:
            return []

    @tool("find_route_by_keywords")
    async def find_route_by_keywords(self, keywords: List[str]) -> Optional[str]:
        """
        Поиск маршрута по ключевым словам. Используйте этот инструмент когда пользователь упоминает место назначения или тип путешествия.

        Args:
            keywords: Список ключевых слов для поиска (например: ["хадж", "мекка", "медина"])

        Returns:
            UUID найденного маршрута или None если не найдено
        """
        route = await self._route_search_repo.find_route_by_keywords(keywords=keywords)
        if route:
            return str(route.id)
        return None


# Функции для создания инструментов (для использования в Langchain)
def create_search_tools(route_search_repo: RouteSearchRepository) -> List:
    """Создает список инструментов для поиска данных"""
    search_tools_instance = SearchTools(route_search_repo)

    # Создаем функции-обертки для каждого инструмента
    async def search_hotels_wrapper(route_id: str, limit: int = 3):
        return await search_tools_instance.search_hotels(route_id, limit)

    async def search_restaurants_wrapper(route_id: str, limit: int = 3):
        return await search_tools_instance.search_restaurants(route_id, limit)

    async def search_amal_templates_wrapper(route_id: str, limit: int = 3):
        return await search_tools_instance.search_amal_templates(route_id, limit)

    async def find_route_wrapper(keywords: List[str]):
        return await search_tools_instance.find_route_by_keywords(keywords)

    # Создаем инструменты с правильными метаданными
    from langchain_core.tools import tool

    tools = [
        tool(search_hotels_wrapper),
        tool(search_restaurants_wrapper),
        tool(search_amal_templates_wrapper),
        tool(find_route_wrapper),
    ]

    return tools
