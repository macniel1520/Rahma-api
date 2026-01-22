from sqladmin import Admin

from app.admin.auth import auth_backend
from app.admin.utils import sync_engine
from app.admin.views import (
    AmalAdmin,
    AmalCategoryAdmin,
    AmalCompletionAdmin,
    AmalTemplateAdmin,
    CountryAdmin,
    EmailVerificationAdmin,
    HotelAdmin,
    IconAdmin,
    LocationAdmin,
    MessageAdmin,
    PasswordResetCodeAdmin,
    RefreshTokenAdmin,
    RestaurantAdmin,
    RouteAdmin,
    RouteImageAdmin,
    UserAdmin,
)


def create_admin_app(app):
    """Create and configure SQLAdmin instance."""

    admin = Admin(
        app=app,
        engine=sync_engine,
        authentication_backend=auth_backend,
        base_url="/admin",
        title="Rahma Admin",
    )

    admin.add_view(UserAdmin)
    admin.add_view(CountryAdmin)
    admin.add_view(RouteAdmin)
    admin.add_view(AmalAdmin)
    admin.add_view(AmalCategoryAdmin)
    admin.add_view(AmalCompletionAdmin)
    admin.add_view(AmalTemplateAdmin)
    admin.add_view(LocationAdmin)
    admin.add_view(HotelAdmin)
    admin.add_view(RestaurantAdmin)
    admin.add_view(IconAdmin)
    admin.add_view(MessageAdmin)
    admin.add_view(RouteImageAdmin)
    admin.add_view(EmailVerificationAdmin)
    admin.add_view(PasswordResetCodeAdmin)
    admin.add_view(RefreshTokenAdmin)

    return admin