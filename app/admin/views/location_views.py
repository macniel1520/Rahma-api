from sqladmin import ModelView

from app.db.models.hotel import Hotel
from app.db.models.location import Location
from app.db.models.restaurant import Restaurant


class LocationAdmin(ModelView, model=Location):
    """Admin view for Location model."""

    name = "Location"
    name_plural = "Locations"
    icon = "fa-solid fa-map-marker-alt"

    column_list = [
        Location.id,
        Location.lat,
        Location.lng,
        Location.createdAt,
        Location.updatedAt,
    ]

    column_details_list = [
        Location.id,
        Location.lat,
        Location.lng,
        Location.createdAt,
        Location.updatedAt,
    ]

    column_sortable_list = [
        Location.createdAt,
        Location.updatedAt,
    ]

    column_labels = {
        Location.id: "ID",
        Location.lat: "Latitude",
        Location.lng: "Longitude",
        Location.createdAt: "Created At",
        Location.updatedAt: "Updated At",
    }


class HotelAdmin(ModelView, model=Hotel):
    """Admin view for Hotel model."""

    name = "Hotel"
    name_plural = "Hotels"
    icon = "fa-solid fa-hotel"

    column_list = [
        Hotel.id,
        Hotel.name,
        Hotel.description,
        Hotel.photoUrl,
        Hotel.avgScore,
        Hotel.avgPrice,
        Hotel.locationId,
        Hotel.routeId,
        Hotel.createdAt,
        Hotel.updatedAt,
    ]

    column_details_list = [
        Hotel.id,
        Hotel.name,
        Hotel.description,
        Hotel.photoUrl,
        Hotel.avgScore,
        Hotel.scoreCount,
        Hotel.avgPrice,
        Hotel.locationId,
        Hotel.routeId,
        Hotel.createdAt,
        Hotel.updatedAt,
    ]

    column_searchable_list = [Hotel.name, Hotel.description]

    column_sortable_list = [
        Hotel.name,
        Hotel.createdAt,
        Hotel.updatedAt,
    ]

    column_labels = {
        Hotel.id: "ID",
        Hotel.name: "Name",
        Hotel.description: "Description",
        Hotel.photoUrl: "Photo URL",
        Hotel.avgScore: "Average Score",
        Hotel.scoreCount: "Score Count",
        Hotel.avgPrice: "Average Price",
        Hotel.locationId: "Location ID",
        Hotel.routeId: "Route ID",
        Hotel.createdAt: "Created At",
        Hotel.updatedAt: "Updated At",
    }


class RestaurantAdmin(ModelView, model=Restaurant):
    """Admin view for Restaurant model."""

    name = "Restaurant"
    name_plural = "Restaurants"
    icon = "fa-solid fa-utensils"

    column_list = [
        Restaurant.id,
        Restaurant.name,
        Restaurant.description,
        Restaurant.photoUrl,
        Restaurant.costLevel,
        Restaurant.isHaram,
        Restaurant.avgScore,
        Restaurant.routeId,
        Restaurant.createdAt,
        Restaurant.updatedAt,
    ]

    column_details_list = [
        Restaurant.id,
        Restaurant.name,
        Restaurant.description,
        Restaurant.photoUrl,
        Restaurant.costLevel,
        Restaurant.isHaram,
        Restaurant.avgScore,
        Restaurant.scoreCount,
        Restaurant.routeId,
        Restaurant.createdAt,
        Restaurant.updatedAt,
    ]

    column_searchable_list = [Restaurant.name, Restaurant.description]

    column_sortable_list = [
        Restaurant.name,
        Restaurant.createdAt,
        Restaurant.updatedAt,
    ]

    column_labels = {
        Restaurant.id: "ID",
        Restaurant.name: "Name",
        Restaurant.description: "Description",
        Restaurant.photoUrl: "Photo URL",
        Restaurant.costLevel: "Cost Level",
        Restaurant.isHaram: "Is Haram",
        Restaurant.avgScore: "Average Score",
        Restaurant.scoreCount: "Score Count",
        Restaurant.routeId: "Route ID",
        Restaurant.createdAt: "Created At",
        Restaurant.updatedAt: "Updated At",
    }
