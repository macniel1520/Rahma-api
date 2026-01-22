from sqladmin import ModelView

from app.db.models.route import Route


class RouteAdmin(ModelView, model=Route):
    """Admin view for Route model."""

    name = "Route"
    name_plural = "Routes"
    icon = "fa-solid fa-route"

    column_list = [
        Route.id,
        Route.name,
        Route.category,
        Route.views,
        Route.photoUrl,
        Route.countryId,
        Route.createdAt,
        Route.updatedAt,
    ]

    column_details_list = [
        Route.id,
        Route.name,
        Route.content,
        Route.category,
        Route.views,
        Route.photoUrl,
        Route.countryId,
        Route.createdAt,
        Route.updatedAt,
    ]

    column_searchable_list = [Route.name, Route.content]

    column_sortable_list = [
        Route.name,
        Route.views,
        Route.createdAt,
        Route.updatedAt,
    ]

    column_labels = {
        Route.id: "ID",
        Route.name: "Name",
        Route.content: "Content",
        Route.category: "Category",
        Route.views: "Views",
        Route.photoUrl: "Photo URL",
        Route.countryId: "Country ID",
        Route.createdAt: "Created At",
        Route.updatedAt: "Updated At",
    }