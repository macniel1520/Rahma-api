from sqladmin import ModelView

from app.db.models.amal_template import AmalTemplate
from app.db.models.email_verification import EmailVerification
from app.db.models.password_reset_code import PasswordResetCode
from app.db.models.refresh import RefreshToken


class AmalTemplateAdmin(ModelView, model=AmalTemplate):
    """Admin view for AmalTemplate model."""

    name = "Amal Template"
    name_plural = "Amal Templates"
    icon = "fa-solid fa-template-icon"

    column_list = [
        AmalTemplate.id,
        AmalTemplate.title,
        AmalTemplate.reccuringRule,
        AmalTemplate.routeId,
        AmalTemplate.createdAt,
        AmalTemplate.updatedAt,
    ]

    column_details_list = [
        AmalTemplate.id,
        AmalTemplate.title,
        AmalTemplate.reccuringRule,
        AmalTemplate.routeId,
        AmalTemplate.createdAt,
        AmalTemplate.updatedAt,
    ]

    column_searchable_list = [AmalTemplate.title]

    column_sortable_list = [
        AmalTemplate.title,
        AmalTemplate.createdAt,
        AmalTemplate.updatedAt,
    ]

    column_labels = {
        AmalTemplate.id: "ID",
        AmalTemplate.title: "Title",
        AmalTemplate.reccuringRule: "Recurring Rule",
        AmalTemplate.routeId: "Route ID",
        AmalTemplate.createdAt: "Created At",
        AmalTemplate.updatedAt: "Updated At",
    }


class EmailVerificationAdmin(ModelView, model=EmailVerification):
    """Admin view for EmailVerification model."""

    name = "Email Verification"
    name_plural = "Email Verifications"
    icon = "fa-solid fa-envelope-check"

    column_list = [
        EmailVerification.id,
        EmailVerification.code,
        EmailVerification.expiresAt,
        EmailVerification.userId,
        EmailVerification.createdAt,
        EmailVerification.updatedAt,
    ]

    column_details_list = [
        EmailVerification.id,
        EmailVerification.code,
        EmailVerification.expiresAt,
        EmailVerification.userId,
        EmailVerification.createdAt,
        EmailVerification.updatedAt,
    ]

    column_searchable_list = [EmailVerification.code]

    column_sortable_list = [
        EmailVerification.expiresAt,
        EmailVerification.createdAt,
        EmailVerification.updatedAt,
    ]

    form_excluded_columns = [
        EmailVerification.code,  
    ]

    column_labels = {
        EmailVerification.id: "ID",
        EmailVerification.code: "Code",
        EmailVerification.expiresAt: "Expires At",
        EmailVerification.userId: "User ID",
        EmailVerification.createdAt: "Created At",
        EmailVerification.updatedAt: "Updated At",
    }


class PasswordResetCodeAdmin(ModelView, model=PasswordResetCode):
    """Admin view for PasswordResetCode model."""

    name = "Password Reset Code"
    name_plural = "Password Reset Codes"
    icon = "fa-solid fa-key"

    column_list = [
        PasswordResetCode.id,
        PasswordResetCode.code,
        PasswordResetCode.expiresAt,
        PasswordResetCode.userId,
        PasswordResetCode.createdAt,
        PasswordResetCode.updatedAt,
    ]

    column_details_list = [
        PasswordResetCode.id,
        PasswordResetCode.code,
        PasswordResetCode.expiresAt,
        PasswordResetCode.userId,
        PasswordResetCode.createdAt,
        PasswordResetCode.updatedAt,
    ]

    column_searchable_list = [PasswordResetCode.code]

    column_sortable_list = [
        PasswordResetCode.expiresAt,
        PasswordResetCode.createdAt,
        PasswordResetCode.updatedAt,
    ]

    form_excluded_columns = [
        PasswordResetCode.code, 
    ]

    column_labels = {
        PasswordResetCode.id: "ID",
        PasswordResetCode.code: "Code",
        PasswordResetCode.expiresAt: "Expires At",
        PasswordResetCode.userId: "User ID",
        PasswordResetCode.createdAt: "Created At",
        PasswordResetCode.updatedAt: "Updated At",
    }


class RefreshTokenAdmin(ModelView, model=RefreshToken):
    """Admin view for RefreshToken model."""

    name = "Refresh Token"
    name_plural = "Refresh Tokens"
    icon = "fa-solid fa-refresh"

    column_list = [
        RefreshToken.id,
        RefreshToken.expiresAt,
        RefreshToken.revokedAt,
        RefreshToken.userId,
        RefreshToken.createdAt,
        RefreshToken.updatedAt,
    ]

    column_details_list = [
        RefreshToken.id,
        RefreshToken.tokenHash,
        RefreshToken.expiresAt,
        RefreshToken.revokedAt,
        RefreshToken.userId,
        RefreshToken.createdAt,
        RefreshToken.updatedAt,
    ]

    column_sortable_list = [
        RefreshToken.expiresAt,
        RefreshToken.revokedAt,
        RefreshToken.createdAt,
        RefreshToken.updatedAt,
    ]

    form_excluded_columns = [
        RefreshToken.tokenHash,  
    ]

    column_labels = {
        RefreshToken.id: "ID",
        RefreshToken.tokenHash: "Token Hash",
        RefreshToken.expiresAt: "Expires At",
        RefreshToken.revokedAt: "Revoked At",
        RefreshToken.userId: "User ID",
        RefreshToken.createdAt: "Created At",
        RefreshToken.updatedAt: "Updated At",
    }