from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views

urlpatterns = [
    path("api/validate/<uuid>/", views.ValidateAPI.as_view()),
]


router = DefaultRouter()
router.register(r"api/track", views.TrackViewSet)
router.register(r"api/stop", views.StopViewSet)
router.register(r"api/school", views.SchoolViewSet)
router.register(r"api/available_date", views.AvailableDateViewSet)
router.register(r"api/date_subscription", views.DateSubscriptionViewSet)
router.register(r"api/responsible", views.ResponsibleViewSet)
router.register(r"api/responsible_list", views.ResponsibleListView)
router.register(r"api/student", views.StudentViewSet)
router.register(r"api/student_list", views.StudentListView)
router.register(r"api/point_of_contact", views.PointOfContactViewSet)

urlpatterns += router.urls
