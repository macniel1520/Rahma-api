from sqladmin import ModelView

from app.db.models.user import User


class UserAdmin(ModelView, model=User):
    """Admin view for User model."""

    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

    column_list = [
        User.id,
        User.email,
        User.name,
        User.isVerified,
        User.isActive,
        User.isSuperuser,
        User.dateOfBirth,
        User.gender,
        User.country,
        User.createdAt,
        User.updatedAt,
    ]

    column_details_list = [
        User.id,
        User.email,
        User.name,
        User.isVerified,
        User.isActive,
        User.isSuperuser,
        User.dateOfBirth,
        User.gender,
        User.country,
        User.avatarUrl,
        User.createdAt,
        User.updatedAt,
    ]

    column_searchable_list = [User.email, User.name]

    column_filters = []

    column_sortable_list = [
        User.email,
        User.name,
        User.createdAt,
        User.updatedAt,
    ]

    form_excluded_columns = [
        User.password,
        User.createdAt,
        User.updatedAt,
    ]

    column_labels = {
        User.id: "ID",
        User.email: "Email",
        User.name: "Name",
        User.isVerified: "Verified",
        User.isActive: "Active",
        User.isSuperuser: "Superuser",
        User.dateOfBirth: "Date of Birth",
        User.avatarUrl: "Avatar URL",
        User.createdAt: "Created At",
        User.updatedAt: "Updated At",
    }
