from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from . import models, serializers


class TrackViewSet(ReadOnlyModelViewSet):
    queryset = models.TrackModel.objects.all()
    serializer_class = serializers.TrackSerializer


class StopViewSet(ReadOnlyModelViewSet):
    queryset = models.StopModel.objects.all()
    serializer_class = serializers.StopSerializer


class SchoolViewSet(ReadOnlyModelViewSet):
    queryset = models.SchoolModel.objects.all()
    serializer_class = serializers.SchoolSerializer


class AvailableDateViewSet(ReadOnlyModelViewSet):
    queryset = models.AvailableDateModel.objects.all()
    serializer_class = serializers.AvailableDateSerializer


class DateSubscriptionViewSet(ModelViewSet):
    queryset = models.DateSubscriptionModel.objects.all()
    serializer_class = serializers.DateSubscriptionSerializer


class ResponsibleViewSet(ModelViewSet):
    queryset = models.TrackModel.objects.all()
    serializer_class = serializers.ResponsibleSerializer


class StudentViewSet(ModelViewSet):
    queryset = models.StudentModel.objects.all()
    serializer_class = serializers.StudentSerializer
