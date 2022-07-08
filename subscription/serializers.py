from rest_framework.serializers import ModelSerializer

from . import models


class TrackSerializer(ModelSerializer):
    class Meta:
        model = models.TrackModel


class StopSerializer(ModelSerializer):
    class Meta:
        model = models.StopModel


class SchoolSerializer(ModelSerializer):
    class Meta:
        model = models.SchoolModel


class AvailableDateSerializer(ModelSerializer):
    class Meta:
        model = models.AvailableDateModel


class DateSubscriptionSerializer(ModelSerializer):
    class Meta:
        model = models.DateSubscriptionModel


class ResponsibleSerializer(ModelSerializer):
    class Meta:
        model = models.ResponsibleModel


class StudentSerializer(ModelSerializer):
    class Meta:
        model = models.StudentModel
