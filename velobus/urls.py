from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "",
        TemplateView.as_view(
            template_name="subscription.html", extra_context={"is_debug": settings.DEBUG}
        ),
    ),
    path("subscription/", include("subscription.urls"), name="subscription"),
]
