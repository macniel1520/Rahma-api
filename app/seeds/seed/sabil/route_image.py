from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models.route_image import RouteImage
from app.db.models.route import Route
from app.seeds.factories import RouteImageFactory


async def create_route_image(
    session: AsyncSession,
    route: Route,
    url: str,
) -> RouteImage:
    """Create a route image with the given URL."""

    existing_image = await session.scalar(
        select(RouteImage).where(RouteImage.routeId == route.id, RouteImage.url == url)
    )
    if existing_image:
        return existing_image

    image = RouteImageFactory.build(route=route)
    image.url = url

    session.add(image)
    await session.commit()
    await session.refresh(image)
    return image


async def create_route_images(
    session: AsyncSession,
    route: Route,
    urls: list[str],
) -> list[RouteImage]:
    """Create multiple route images."""

    images = []
    for url in urls:
        image = await create_route_image(session, route, url)
        images.append(image)

    return images


ROUTE_IMAGES_DATA = {
    # Саудовская Аравия
    "Сафа и Марва": [
        "https://s3.geometria.ru/rahma-test/countries/saudi-arabia/as_safa_al_marva_mekka.webp",
    ],
    "Масджид аль-Харам": [
        "https://s3.geometria.ru/rahma-test/countries/saudi-arabia/mechet_al_haram.webp",
    ],
    "Мина (долина палаток)": [
        "https://s3.geometria.ru/rahma-test/countries/saudi-arabia/mina.webp",
    ],
    # Иран
    "Кум — мавзолей Фатимы Масумы": [
        "https://s3.geometria.ru/rahma-test/countries/iran/mavzoley_fatimi_masume.webp",
    ],
    "Мешхед — мавзолей имама Резы": [
        "https://s3.geometria.ru/rahma-test/countries/iran/mavzoley_imama_rezi.webp",
    ],
    "Шираз — Шах-Черах": [
        "https://s3.geometria.ru/rahma-test/countries/iran/mavzoley_shah_cherah.webp",
    ],
    # Ирак
    "Кадимия (Багдад) — Аль-Кадимейн": [
        "https://s3.geometria.ru/rahma-test/countries/iraq/al_kadhimiya_mosque.webp",
    ],
    "Кербела — мавзолей имама Хусейна": [
        "https://s3.geometria.ru/rahma-test/countries/iraq/kerbela.webp",
    ],
    "Наджаф — мавзолей имама Али": [
        "https://s3.geometria.ru/rahma-test/countries/iraq/mechet_imama_ali.webp",
    ],
    # Египет
    "Каир — мечеть и университет Аль-Азхар": [
        "https://s3.geometria.ru/rahma-test/countries/egypt/kair_al_azhar.webp",
    ],
    "Каир — мечеть Аль-Хусейна": [
        "https://s3.geometria.ru/rahma-test/countries/egypt/kair_mechet_al_husein.webp",
    ],
    "Каир — мечеть Сайида Зейнаб": [
        "https://s3.geometria.ru/rahma-test/countries/egypt/mechet_sayeda_zainab_kair.webp",
    ],
}


async def create_route_images_sabil(
    session: AsyncSession,
    routes: list[Route],
) -> list[RouteImage]:
    """Create standard sabil route images for given routes."""

    all_images = []
    for route in routes:
        urls = ROUTE_IMAGES_DATA.get(route.name, [])
        if urls:
            images = await create_route_images(session, route, urls)
            all_images.extend(images)

    return all_images
