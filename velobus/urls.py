from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        TemplateView.as_view(
            template_name="subscription.html", extra_context={"is_debug": settings.DEBUG}
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
]
