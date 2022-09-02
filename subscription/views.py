from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from django.core.mail import send_mail
from django.conf import settings

from . import models, serializers


def send_welcome_mail(
    person: str, uuid: str, recipient: str, track_id: int = None
) -> int:
    subject = "Inscription vélobus"
    base_url = (
        f"https://{settings.ALLOWED_HOSTS[0]}"
        if settings.ALLOWED_HOSTS
        else "http://localhost"
    )
    contacts = (
        [
            f"Référent du tracé ({contact.track.name}) : {contact.last_name} {contact.first_name} ({contact.phone_number})."
            for contact in models.ResponsibleModel.filter(
                track__id=track_id, is_point_of_contact=True
            )
        ]
        if track_id
        else []
    )

    raw_message = (
        """Bonjour,
        Merci pour votre inscription. Retrouvez toutes les informations concernant votre inscription à l'adresse suivante:
        """
        + base_url
        + f"/#/{person}/1/{uuid}"
        + """
        """
        + "\n".join(contacts)
        + """
        L'équipe Vélobus
        """
    )
    html_message = f"<p>Bonjour</p><p>Merci pour votre inscription. Retrouvez toutes les informations concernant votre inscription par le lien suivant: <a href='{base_url}/#/{person}/1/{uuid}'>inscription</a>.<br>{'<br>'.join(contacts)}</p><p>Cordialement<br>L'équipe Vélobus</p>"

    return send_mail(
        subject=subject,
        message=raw_message,
        from_email=None,
        recipient_list=[recipient],
        fail_silently=True,
        html_message=html_message,
    )


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


class ResponsibleViewSet(
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = models.ResponsibleModel.objects.all()
    serializer_class = serializers.ResponsibleSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        send_welcome_mail("responsible", instance.uuid, instance.email)


class ResponsibleListView(ReadOnlyModelViewSet):
    queryset = models.ResponsibleModel.objects.all()
    serializer_class = serializers.ResponsibleSerializer
    permission_classes = [IsAuthenticated]


class PointOfContactViewSet(ReadOnlyModelViewSet):
    queryset = models.ResponsibleModel.objects.filter(is_point_of_contact=True)
    serializer_class = serializers.ResponsibleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["track"]


class StudentViewSet(
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    queryset = models.StudentModel.objects.all()
    serializer_class = serializers.StudentSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        track_id = instance.track.id
        send_welcome_mail("student", instance.uuid, instance.email, track_id)


class StudentListView(ReadOnlyModelViewSet):
    queryset = models.ResponsibleModel.objects.all()
    serializer_class = serializers.ResponsibleSerializer
    permission_classes = [IsAuthenticated]
