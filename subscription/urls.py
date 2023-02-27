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
