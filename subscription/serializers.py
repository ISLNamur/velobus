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

from rest_framework.serializers import ModelSerializer

from . import models


class TrackSerializer(ModelSerializer):
    class Meta:
        model = models.TrackModel
        fields = "__all__"


class StopSerializer(ModelSerializer):
    class Meta:
        model = models.StopModel
        fields = "__all__"


class SchoolSerializer(ModelSerializer):
    class Meta:
        model = models.SchoolModel
        fields = "__all__"


class AvailableDateSerializer(ModelSerializer):
    class Meta:
        model = models.AvailableDateModel
        fields = "__all__"


class DateSubscriptionSerializer(ModelSerializer):
    class Meta:
        model = models.DateSubscriptionModel
        fields = "__all__"


class ResponsibleSerializer(ModelSerializer):
    class Meta:
        model = models.ResponsibleModel
        fields = "__all__"


class ResponsibleDepthSerializer(ModelSerializer):
    class Meta:
        model = models.ResponsibleModel
        fields = "__all__"
        depth = 1


class StudentSerializer(ModelSerializer):
    class Meta:
        model = models.StudentModel
        fields = "__all__"


class StudentDepthSerializer(ModelSerializer):
    class Meta:
        model = models.StudentModel
        fields = "__all__"
        depth = 1
