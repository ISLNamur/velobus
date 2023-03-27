# Velobus
# Copyright (C) 2023  Manuel Tondeur

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        TemplateView.as_view(
            template_name="subscription.html",
            extra_context={
                "is_debug": settings.DEBUG,
                "form_title": settings.FORM_TITLE,
                "schedule_comment": settings.SCHEDULE_COMMENT,
                "map_center": settings.MAP_CENTER,
                "map_zoom": settings.MAP_ZOOM,
                "end_text": settings.END_TEXT,
            },
        ),
    ),
    path("subscription/", include("subscription.urls"), name="subscription"),
    path(
        "accounts/login/",
        LoginView.as_view(
            template_name="auth.html",
            redirect_authenticated_user=True,
        ),
        name="auth",
    ),
    path("logout/", LogoutView.as_view(next_page="auth")),
    path("accounts/password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path(
        "accounts/password_reset_done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/done/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
