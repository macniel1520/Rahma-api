from sqladmin import ModelView

from app.db.models.amal import Amal
from app.db.models.amal_category import AmalCategory
from app.db.models.amal_completion import AmalCompletion


class AmalAdmin(ModelView, model=Amal):
    """Admin view for Amal model."""

    name = "Amal"
    name_plural = "Amals"
    icon = "fa-solid fa-star"

    column_list = [
        Amal.id,
        Amal.title,
        Amal.date,
        Amal.time,
        Amal.reccuringRule,
        Amal.amalCategoryId,
        Amal.userId,
        Amal.iconId,
        Amal.createdAt,
        Amal.updatedAt,
    ]

    column_details_list = [
        Amal.id,
        Amal.title,
        Amal.date,
        Amal.time,
        Amal.reccuringRule,
        Amal.amalCategoryId,
        Amal.userId,
        Amal.iconId,
        Amal.createdAt,
        Amal.updatedAt,
    ]

    column_searchable_list = [Amal.title]

    column_sortable_list = [
        Amal.title,
        Amal.date,
        Amal.createdAt,
        Amal.updatedAt,
    ]

    column_labels = {
        Amal.id: "ID",
        Amal.title: "Title",
        Amal.date: "Date",
        Amal.time: "Time",
        Amal.reccuringRule: "Recurring Rule",
        Amal.amalCategoryId: "Category ID",
        Amal.userId: "User ID",
        Amal.iconId: "Icon ID",
        Amal.createdAt: "Created At",
        Amal.updatedAt: "Updated At",
    }


class AmalCategoryAdmin(ModelView, model=AmalCategory):
    """Admin view for AmalCategory model."""

    name = "Amal Category"
    name_plural = "Amal Categories"
    icon = "fa-solid fa-tags"

    column_list = [
        AmalCategory.id,
        AmalCategory.name,
        AmalCategory.createdAt,
        AmalCategory.updatedAt,
    ]

    column_details_list = [
        AmalCategory.id,
        AmalCategory.name,
        AmalCategory.createdAt,
        AmalCategory.updatedAt,
    ]

    column_searchable_list = [AmalCategory.name]

    column_sortable_list = [
        AmalCategory.name,
        AmalCategory.createdAt,
        AmalCategory.updatedAt,
    ]

    column_labels = {
        AmalCategory.id: "ID",
        AmalCategory.name: "Name",
        AmalCategory.createdAt: "Created At",
        AmalCategory.updatedAt: "Updated At",
    }


class AmalCompletionAdmin(ModelView, model=AmalCompletion):
    """Admin view for AmalCompletion model."""

    name = "Amal Completion"
    name_plural = "Amal Completions"
    icon = "fa-solid fa-check-circle"

    column_list = [
        AmalCompletion.id,
        AmalCompletion.date,
        AmalCompletion.completedAt,
        AmalCompletion.amalId,
        AmalCompletion.userId,
        AmalCompletion.createdAt,
        AmalCompletion.updatedAt,
    ]

    column_details_list = [
        AmalCompletion.id,
        AmalCompletion.date,
        AmalCompletion.completedAt,
        AmalCompletion.amalId,
        AmalCompletion.userId,
        AmalCompletion.createdAt,
        AmalCompletion.updatedAt,
    ]

    column_sortable_list = [
        AmalCompletion.date,
        AmalCompletion.completedAt,
        AmalCompletion.createdAt,
        AmalCompletion.updatedAt,
    ]

    column_labels = {
        AmalCompletion.id: "ID",
        AmalCompletion.date: "Date",
        AmalCompletion.completedAt: "Completed At",
        AmalCompletion.amalId: "Amal ID",
        AmalCompletion.userId: "User ID",
        AmalCompletion.createdAt: "Created At",
        AmalCompletion.updatedAt: "Updated At",
    }
