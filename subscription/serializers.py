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
