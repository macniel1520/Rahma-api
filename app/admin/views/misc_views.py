from sqladmin import ModelView

from app.db.models.icon import Icon
from app.db.models.message import Message
from app.db.models.route_image import RouteImage


class IconAdmin(ModelView, model=Icon):
    """Admin view for Icon model."""

    name = "Icon"
    name_plural = "Icons"
    icon = "fa-solid fa-image"

    column_list = [
        Icon.id,
        Icon.url,
        Icon.createdAt,
        Icon.updatedAt,
    ]

    column_details_list = [
        Icon.id,
        Icon.url,
        Icon.createdAt,
        Icon.updatedAt,
    ]

    column_sortable_list = [
        Icon.createdAt,
        Icon.updatedAt,
    ]

    column_labels = {
        Icon.id: "ID",
        Icon.url: "URL",
        Icon.createdAt: "Created At",
        Icon.updatedAt: "Updated At",
    }


class MessageAdmin(ModelView, model=Message):
    """Admin view for Message model."""

    name = "Message"
    name_plural = "Messages"
    icon = "fa-solid fa-envelope"

    column_list = [
        Message.id,
        Message.content,
        Message.role,
        Message.userId,
        Message.createdAt,
        Message.updatedAt,
    ]

    column_details_list = [
        Message.id,
        Message.content,
        Message.role,
        Message.userId,
        Message.createdAt,
        Message.updatedAt,
    ]

    column_searchable_list = [Message.content]

    column_sortable_list = [
        Message.createdAt,
        Message.updatedAt,
    ]

    column_labels = {
        Message.id: "ID",
        Message.content: "Content",
        Message.role: "Role",
        Message.userId: "User ID",
        Message.createdAt: "Created At",
        Message.updatedAt: "Updated At",
    }


class RouteImageAdmin(ModelView, model=RouteImage):
    """Admin view for RouteImage model."""

    name = "Route Image"
    name_plural = "Route Images"
    icon = "fa-solid fa-images"

    column_list = [
        RouteImage.id,
        RouteImage.url,
        RouteImage.routeId,
        RouteImage.createdAt,
        RouteImage.updatedAt,
    ]

    column_details_list = [
        RouteImage.id,
        RouteImage.url,
        RouteImage.routeId,
        RouteImage.createdAt,
        RouteImage.updatedAt,
    ]

    column_sortable_list = [
        RouteImage.createdAt,
        RouteImage.updatedAt,
    ]

    column_labels = {
        RouteImage.id: "ID",
        RouteImage.url: "URL",
        RouteImage.routeId: "Route ID",
        RouteImage.createdAt: "Created At",
        RouteImage.updatedAt: "Updated At",
    }