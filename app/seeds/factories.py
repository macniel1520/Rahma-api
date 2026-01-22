import datetime
import random
import uuid

import factory
from faker import Faker

from app.db.models.amal import Amal
from app.db.models.amal_category import AmalCategory
from app.db.models.amal_completion import AmalCompletion
from app.db.models.amal_template import AmalTemplate
from app.db.models.country import Country
from app.db.models.enums import Category, CostLevel, ReccuringRule
from app.db.models.hotel import Hotel
from app.db.models.icon import Icon
from app.db.models.location import Location
from app.db.models.restaurant import Restaurant
from app.db.models.route import Route
from app.db.models.route_image import RouteImage

fake = Faker()


class CountryFactory(factory.Factory):
    class Meta:
        model = Country

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.LazyFunction(lambda: fake.country())
    photoUrl = factory.LazyFunction(lambda: fake.image_url(width=1200, height=800))


class RouteFactory(factory.Factory):
    class Meta:
        model = Route

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.LazyFunction(lambda: fake.sentence(nb_words=3).rstrip("."))
    content = factory.LazyFunction(lambda: "\n\n".join(fake.paragraphs(nb=3)))
    views = factory.LazyFunction(lambda: random.randint(0, 250_000))
    photoUrl = factory.LazyFunction(lambda: fake.url())
    category = factory.LazyFunction(lambda: random.choice(list(Category)))

    country = factory.SubFactory(CountryFactory)


class RouteImageFactory(factory.Factory):
    class Meta:
        model = RouteImage

    id = factory.LazyFunction(uuid.uuid4)
    url = factory.LazyFunction(lambda: fake.image_url(width=1600, height=900))
    route = factory.SubFactory(RouteFactory)


class RestaurantFactory(factory.Factory):
    class Meta:
        model = Restaurant

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.LazyFunction(lambda: fake.company())
    description = factory.LazyFunction(lambda: fake.paragraph(nb_sentences=4))
    photoUrl = factory.LazyFunction(lambda: fake.image_url(width=1200, height=800))
    avgScore = factory.LazyFunction(lambda: round(random.uniform(3.0, 5.0), 1))
    scoreCount = factory.LazyFunction(lambda: random.randint(0, 20_000))
    isHaram = factory.LazyFunction(lambda: random.choice([True, False]))
    costLevel = factory.LazyFunction(lambda: random.choice(list(CostLevel)))

    route = factory.SubFactory(RouteFactory)


class LocationFactory(factory.Factory):
    class Meta:
        model = Location

    id = factory.LazyFunction(uuid.uuid4)
    lat = factory.LazyFunction(lambda: f"{random.uniform(-90, 90):.6f}")
    lng = factory.LazyFunction(lambda: f"{random.uniform(-180, 180):.6f}")


class HotelFactory(factory.Factory):
    class Meta:
        model = Hotel

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.LazyFunction(lambda: f"{fake.company()} Hotel")
    description = factory.LazyFunction(lambda: fake.paragraph(nb_sentences=5))
    photoUrl = factory.LazyFunction(lambda: fake.image_url(width=1200, height=800))
    avgScore = factory.LazyFunction(lambda: round(random.uniform(3.0, 5.0), 1))
    scoreCount = factory.LazyFunction(lambda: random.randint(0, 20_000))
    avgPrice = factory.LazyFunction(lambda: round(random.uniform(30, 400), 2))

    route = factory.SubFactory(RouteFactory)
    location = factory.SubFactory(LocationFactory)


class AmalTemplateFactory(factory.Factory):
    class Meta:
        model = AmalTemplate

    id = factory.LazyFunction(uuid.uuid4)
    title = factory.LazyFunction(lambda: fake.sentence(nb_words=4).rstrip("."))
    reccuringRule = factory.LazyFunction(lambda: random.choice(list(ReccuringRule)))

    route = factory.SubFactory(RouteFactory)


class IconFactory(factory.Factory):
    class Meta:
        model = Icon

    id = factory.LazyFunction(uuid.uuid4)
    url = factory.LazyFunction(lambda: fake.image_url(width=128, height=128))


class AmalCategoryFactory(factory.Factory):
    class Meta:
        model = AmalCategory

    id = factory.LazyFunction(uuid.uuid4)
    name = factory.LazyFunction(
        lambda: random.choice(
            ["Намаз", "Дуа", "Зикр", "Чтение Корана", "Садака", "Пост", "Тахаджуд"]
        )
    )


class AmalFactory(factory.Factory):
    class Meta:
        model = Amal

    id = factory.LazyFunction(uuid.uuid4)
    title = factory.LazyFunction(
        lambda: random.choice(
            [
                "Утренний намаз",
                "Зухр намаз",
                "Аср намаз",
                "Магриб намаз",
                "Иша намаз",
                "Чтение Корана",
                "Утренние азкары",
                "Вечерние азкары",
                "Истигфар 100 раз",
                "Салават 100 раз",
            ]
        )
    )
    date = factory.LazyFunction(lambda: datetime.date.today())
    time = factory.LazyFunction(
        lambda: datetime.time(random.randint(4, 22), random.randint(0, 59))
    )
    reccuringRule = factory.LazyFunction(lambda: random.choice(list(ReccuringRule)))

    icon = factory.SubFactory(IconFactory)
    category = factory.SubFactory(AmalCategoryFactory)


class AmalCompletionFactory(factory.Factory):
    class Meta:
        model = AmalCompletion

    id = factory.LazyFunction(uuid.uuid4)
    date = factory.LazyFunction(
        lambda: datetime.date.today() - datetime.timedelta(days=random.randint(0, 7))
    )
    completedAt = factory.LazyFunction(
        lambda: datetime.datetime.now()
        - datetime.timedelta(
            days=random.randint(0, 7),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )
    )
