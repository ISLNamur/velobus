from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = []


router = DefaultRouter()
router.register(r"api/track", views.TrackViewSet)
router.register(r"api/stop", views.StopViewSet)
router.register(r"api/school", views.SchoolViewSet)
router.register(r"api/available_date", views.AvailableDateViewSet)
router.register(r"api/date_subscription", views.DateSubscriptionViewSet)
router.register(r"api/responsible", views.ResponsibleViewSet)
router.register(r"api/student", views.StudentViewSet)

urlpatterns += router.urls
