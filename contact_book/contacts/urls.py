from django.urls import path
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from .views import (
    ContactListView,
    ContactCreateView,
    ContactUpdateView,
    ContactDeleteView,
    ContactAjaxDatatableView,
    register_view,
    login_view,
    logout_view,
    manage_users,
    change_user_role
)

urlpatterns = [
    # Authentication URLs
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    # Password reset URLs
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="registration/password_reset_form.html"
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    # CRUD contact urls
    path("", ContactListView.as_view(), name="contact_list"),
    path("api/contacts/", ContactAjaxDatatableView.as_view(), name="contact_data"),
    path("create/", ContactCreateView.as_view(), name="contact_create"),
    path("update/<int:pk>/", ContactUpdateView.as_view(), name="contact_update"),
    path("delete/<int:pk>/", ContactDeleteView.as_view(), name="contact_delete"),
    # Admin URLs
    path("manage-users/", manage_users, name="manage_users"),
    path(
        "change-user-role/<int:user_id>/<str:new_role>/",
        change_user_role,
        name="change_user_role",
    ),
]
