from __future__ import annotations

from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, Field


class PanelUser(BaseModel):
    id: UUID
    email: str
    name: str
    is_superuser: bool = Field(alias="isSuperuser")

    model_config = {"populate_by_name": True}


class PanelAuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: Literal["bearer"] = "bearer"
    user: PanelUser


class UploadResponse(BaseModel):
    object_key: str
    public_url: str


class OptionItem(BaseModel):
    value: str
    label: str


class AdminSection(BaseModel):
    id: str
    label: str
    kind: Literal["page", "group"] = "page"


class ResourceField(BaseModel):
    name: str
    label: str
    type: Literal["text", "textarea", "number", "select", "boolean", "upload", "hidden"]
    required: bool = False
    placeholder: str | None = None
    help_text: str | None = Field(default=None, alias="helpText")
    bind: str | None = None
    options: list[OptionItem] = Field(default_factory=list)
    options_resource: str | None = Field(default=None, alias="optionsResource")
    accept: list[str] = Field(default_factory=list)
    min: float | None = None
    max: float | None = None
    step: float | None = None
    default: Any = None

    model_config = {"populate_by_name": True}


class ResourceColumn(BaseModel):
    key: str
    label: str
    kind: Literal["text", "number", "boolean", "image"] = "text"


class ResourceDescriptor(BaseModel):
    id: str
    label: str
    singular_label: str = Field(alias="singularLabel")
    section: str
    entity_type: str = Field(alias="entityType")
    create_label: str = Field(alias="createLabel")
    empty_state: str = Field(alias="emptyState")
    primary_field: str = Field(alias="primaryField")
    image_field: str | None = Field(default=None, alias="imageField")
    description_field: str | None = Field(default=None, alias="descriptionField")
    fields: list[ResourceField]
    columns: list[ResourceColumn]

    model_config = {"populate_by_name": True}


class BootstrapPayload(BaseModel):
    user: PanelUser
    sections: list[AdminSection]
    resources: list[ResourceDescriptor]
    actions: dict[str, Any]


class DashboardSummary(BaseModel):
    countries: int
    routes: int
    hotels: int
    restaurants: int


class CountryItem(BaseModel):
    id: UUID
    name: str
    photo_url: str = Field(alias="photoUrl")
    routes_count: int

    model_config = {"populate_by_name": True}


class CountryCreate(BaseModel):
    name: str
    photoUrl: str


class RouteItem(BaseModel):
    id: UUID
    name: str
    content: str
    photo_url: str = Field(alias="photoUrl")
    views: int
    category: str
    country_id: UUID = Field(alias="countryId")
    country_name: str
    hotels_count: int
    restaurants_count: int

    model_config = {"populate_by_name": True}


class RouteCreate(BaseModel):
    name: str
    content: str
    category: str
    countryId: UUID
    photoUrl: str
    views: int = 0


class HotelItem(BaseModel):
    id: UUID
    name: str
    description: str
    photo_url: str = Field(alias="photoUrl")
    avg_score: float = Field(alias="avgScore")
    score_count: int = Field(alias="scoreCount")
    avg_price: float = Field(alias="avgPrice")
    route_id: UUID = Field(alias="routeId")
    route_name: str
    location_id: UUID | None = Field(alias="locationId")
    lat: str | None = None
    lng: str | None = None

    model_config = {"populate_by_name": True}


class HotelCreate(BaseModel):
    name: str
    description: str
    photoUrl: str
    avgScore: float
    scoreCount: int
    avgPrice: float
    routeId: UUID
    lat: float
    lng: float


class RestaurantItem(BaseModel):
    id: UUID
    name: str
    description: str
    photo_url: str = Field(alias="photoUrl")
    avg_score: float = Field(alias="avgScore")
    score_count: int = Field(alias="scoreCount")
    is_haram: bool = Field(alias="isHaram")
    cost_level: str = Field(alias="costLevel")
    route_id: UUID = Field(alias="routeId")
    route_name: str

    model_config = {"populate_by_name": True}


class RestaurantCreate(BaseModel):
    name: str
    description: str
    photoUrl: str
    avgScore: float
    scoreCount: int
    isHaram: bool
    costLevel: str
    routeId: UUID


class RouteImageItem(BaseModel):
    id: UUID
    url: str
    route_id: UUID = Field(alias="routeId")
    route_name: str

    model_config = {"populate_by_name": True}


class RouteImageCreate(BaseModel):
    url: str
    routeId: UUID


class IconItem(BaseModel):
    id: UUID
    url: str


class IconCreate(BaseModel):
    url: str


class AmalCategoryItem(BaseModel):
    id: UUID
    name: str


class AmalCategoryCreate(BaseModel):
    name: str


class AmalTemplateItem(BaseModel):
    id: UUID
    title: str
    recurring_rule: str = Field(alias="reccuringRule")
    route_id: UUID = Field(alias="routeId")
    route_name: str

    model_config = {"populate_by_name": True}


class AmalTemplateCreate(BaseModel):
    title: str
    reccuringRule: str
    routeId: UUID


class ActionExecuteIn(BaseModel):
    method: str
    path: str
    path_params: dict[str, Any] = Field(default_factory=dict, alias="pathParams")
    query_params: dict[str, Any] = Field(default_factory=dict, alias="queryParams")
    headers: dict[str, str] = Field(default_factory=dict)
    json_body: Any = Field(default=None, alias="jsonBody")
    use_current_auth: bool = Field(default=True, alias="useCurrentAuth")

    model_config = {"populate_by_name": True}


class ActionExecuteOut(BaseModel):
    status_code: int = Field(alias="statusCode")
    headers: dict[str, str]
    body: Any
    is_json: bool = Field(alias="isJson")

    model_config = {"populate_by_name": True}
