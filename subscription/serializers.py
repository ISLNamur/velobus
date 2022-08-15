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


class StudentSerializer(ModelSerializer):
    class Meta:
        model = models.StudentModel
        fields = "__all__"
