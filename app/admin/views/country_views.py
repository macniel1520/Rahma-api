from sqladmin import ModelView
        
from app.db.models.country import Country


class CountryAdmin(ModelView, model=Country):
    """Admin view for Country model."""

    name = "Country"
    name_plural = "Countries"
    icon = "fa-solid fa-flag"

  
    column_list = [
        Country.id,
        Country.name,
        Country.photoUrl,
        Country.createdAt,
        Country.updatedAt,
    ]

    column_details_list = [
        Country.id,
        Country.name,
        Country.photoUrl,
        Country.createdAt,
        Country.updatedAt,
    ]

    column_searchable_list = [Country.name]

    column_sortable_list = [
        Country.name,
        Country.createdAt,
        Country.updatedAt,
    ]

    column_labels = {
        Country.id: "ID",
        Country.name: "Name",
        Country.photoUrl: "Photo URL",
        Country.createdAt: "Created At",
        Country.updatedAt: "Updated At",
    }