from typing import Any, Dict, List

from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain_core.tools import tool
from langchain_deepseek import ChatDeepSeek

from app.api.v1.schemas.sabil.amal_template_schema import AmalTemplateRead
from app.api.v1.schemas.sabil.hotel_schema import HotelRead
from app.api.v1.schemas.sabil.restaurant_schema import RestaurantRead
from app.core.config import settings
from app.db.cruds.route_search_repository import RouteSearchRepository
from app.services.assadik.constants import SYSTEM_PROMPT
from app.utils.structlog_config import logger


class AIAgentService:
    def __init__(self, route_search_repo: RouteSearchRepository):
        self._route_search_repo = route_search_repo
        self._llm = ChatDeepSeek(
            model=settings.ai.model,
            api_key=settings.ai.api_key,
            temperature=0.3,
        )
        self._tools = self._create_tools()
        self._ui_data = None
        self._current_route_id = None

        @wrap_tool_call
        async def process_tools(request, handler):
            await self._handle_tool_call(request.tool_call)
            tool_result = await handler(request)
            return tool_result

        self._agent = create_agent(
            model=self._llm,
            tools=self._tools,
            system_prompt=SYSTEM_PROMPT,
            middleware=[process_tools],
        )

    def _create_tools(self) -> List:
        """Создает инструменты для агента"""

        @tool
        def find_and_show_route_data(
            location: str,
            data_types: List[str] = ["hotels", "restaurants", "amal_templates"],
        ) -> str:
            """
            Находит маршрут по названию места и показывает соответствующие данные (отели, рестораны, шаблоны амалов).

            Args:
                location: Название места (например: "Мекка", "Медина", "хадж")
                data_types: Типы данных для показа (hotels, restaurants, amal_templates)
            """
            logger.info(
                f"Tool called: find_and_show_route_data with location: {location}, data_types: {data_types}"
            )
            return f"TOOL_CALL:find_and_show:{location}:{','.join(data_types)}"

        return [find_and_show_route_data]

    async def _handle_tool_call(self, tool_call):
        """Обрабатывает вызов инструмента и сохраняет UI данные"""
        try:
            tool_name = tool_call.get("name")
            args = tool_call.get("args", {})

            logger.info(f"Handling tool call: {tool_name} with args: {args}")

            if tool_name == "find_and_show_route_data":
                location = args.get("location", "")
                data_types = args.get(
                    "data_types", ["hotels", "restaurants", "amal_templates"]
                )

                logger.info(
                    f"Finding route and data for location: {location}, data_types: {data_types}"
                )

                # Разбиваем location на ключевые слова для поиска
                keywords = [word.strip() for word in location.split() if word.strip()]
                route = await self._route_search_repo.find_route_by_keywords(
                    keywords=keywords
                )

                if route:
                    logger.info(f"Found route: {route.name} with ID: {route.id}")

                    if not self._ui_data:
                        self._ui_data = {
                            "hotels": [],
                            "restaurants": [],
                            "amal_templates": [],
                        }

                    if "hotels" in data_types:
                        hotels = await self._route_search_repo.search_hotels_by_route(
                            route_id=route.id, limit=10
                        )

                        hotel_data = []
                        for hotel in sorted(
                            hotels, key=lambda h: h.avgScore, reverse=True
                        )[:5]:
                            hotel_read = HotelRead.model_validate(hotel)
                            hotel_data.append(hotel_read.model_dump())
                        self._ui_data["hotels"].extend(hotel_data)
                        logger.info(f"Found {len(hotel_data)} top hotels")

                    if "restaurants" in data_types:
                        restaurants = (
                            await self._route_search_repo.search_restaurants_by_route(
                                route_id=route.id, limit=10
                            )
                        )
                        # Сортируем по рейтингу и берем топ-5
                        restaurant_data = []
                        for restaurant in sorted(
                            restaurants, key=lambda r: r.avgScore, reverse=True
                        )[:5]:
                            restaurant_read = RestaurantRead.model_validate(restaurant)
                            restaurant_data.append(restaurant_read.model_dump())
                        self._ui_data["restaurants"].extend(restaurant_data)
                        logger.info(f"Found {len(restaurant_data)} top restaurants")

                    if "amal_templates" in data_types:
                        templates = await self._route_search_repo.search_amal_templates_by_route(
                            route_id=route.id, limit=5
                        )
                        template_data = []
                        for template in templates:
                            template_read = AmalTemplateRead.model_validate(template)
                            template_data.append(template_read.model_dump())
                        self._ui_data["amal_templates"].extend(template_data)
                        logger.info(f"Found {len(template_data)} amal templates")

                else:
                    logger.info(f"No route found for location: {location}")

            logger.info(f"Current UI data: {self._ui_data}")

        except Exception as e:
            logger.error(f"Error handling tool call {tool_call}: {e}")
            import traceback

            logger.error(f"Traceback: {traceback.format_exc()}")

    async def process_message(self, message: str) -> Dict[str, Any]:
        """
        Обрабатывает сообщение пользователя и возвращает ответ с UI данными

        Args:
            message: Сообщение пользователя

        Returns:
            Словарь с текстом ответа и данными для UI
        """
        self._ui_data = None
        self._current_route_id = None

        try:
            result = await self._agent.ainvoke(
                {"messages": [{"role": "user", "content": message}]}
            )

            messages = result.get("messages", [])
            response_text = ""

            for msg in reversed(messages):
                if msg.__class__.__name__ == "AIMessage" and msg.content:
                    response_text = msg.content
                    break

            ui_data = None
            if self._ui_data:
                ui_data = {k: v for k, v in self._ui_data.items() if v}
                if not ui_data:
                    ui_data = None

            if ui_data and response_text:
                mentioned_data = False
                if ui_data.get("hotels"):
                    for hotel in ui_data["hotels"]:
                        if hotel.get("name", "").lower() in response_text.lower():
                            mentioned_data = True
                            break
                if ui_data.get("restaurants"):
                    for restaurant in ui_data["restaurants"]:
                        if restaurant.get("name", "").lower() in response_text.lower():
                            mentioned_data = True
                            break
                if ui_data.get("amal_templates"):
                    for template in ui_data["amal_templates"]:
                        if template.get("title", "").lower() in response_text.lower():
                            mentioned_data = True
                            break

                if not mentioned_data:
                    logger.warning(
                        "Agent didn't mention UI data in response, appending it"
                    )
                    if ui_data.get("hotels"):
                        response_text += "\n\n**Найденные отели:**\n"
                        for i, hotel in enumerate(ui_data["hotels"][:3], 1):
                            response_text += (
                                f"{i}. {hotel['name']} (рейтинг: {hotel['avgScore']})\n"
                            )
                    if ui_data.get("restaurants"):
                        response_text += "\n\n**Найденные рестораны:**\n"
                        for i, restaurant in enumerate(ui_data["restaurants"][:3], 1):
                            response_text += f"{i}. {restaurant['name']} (рейтинг: {restaurant['avgScore']})\n"
                    if ui_data.get("amal_templates"):
                        response_text += "\n\n**Шаблоны амалов:**\n"
                        for i, template in enumerate(ui_data["amal_templates"][:3], 1):
                            response_text += f"{i}. {template['title']}\n"

            return {
                "content": response_text,
                "ui": ui_data,
            }

        except Exception as e:
            logger.error(f"Error processing message with AI agent: {e}")
            return {
                "content": "Извините, произошла ошибка при обработке вашего сообщения.",
                "ui": None,
            }
