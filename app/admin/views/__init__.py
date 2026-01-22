# Admin views

from app.admin.views.amal_views import AmalAdmin, AmalCategoryAdmin, AmalCompletionAdmin
from app.admin.views.auth_views import (
    AmalTemplateAdmin,
    EmailVerificationAdmin,
    PasswordResetCodeAdmin,
    RefreshTokenAdmin,
)
from app.admin.views.country_views import CountryAdmin
from app.admin.views.location_views import HotelAdmin, LocationAdmin, RestaurantAdmin
from app.admin.views.misc_views import IconAdmin, MessageAdmin, RouteImageAdmin
from app.admin.views.route_views import RouteAdmin
from app.admin.views.user_views import UserAdmin

__all__ = [
    # User views
    "UserAdmin",
    # Country views
    "CountryAdmin",
    # Route views
    "RouteAdmin",
    # Amal views
    "AmalAdmin",
    "AmalCategoryAdmin",
    "AmalCompletionAdmin",
    # Location views
    "LocationAdmin",
    "HotelAdmin",
    "RestaurantAdmin",
    # Misc views
    "IconAdmin",
    "MessageAdmin",
    "RouteImageAdmin",
    # Auth views
    "AmalTemplateAdmin",
    "EmailVerificationAdmin",
    "PasswordResetCodeAdmin",
    "RefreshTokenAdmin",
]