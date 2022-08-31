from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from django.core.mail import send_mail
from django.conf import settings

from . import models, serializers


def send_welcome_mail(person: str, uuid: str, recipient: str) -> int:
    subject = "Inscription vélobus"
    base_url = (
        f"https://{settings.ALLOWED_HOSTS[0]}"
        if settings.ALLOWED_HOSTS
        else "http://localhost"
    )
    raw_message = (
        """Bonjour,
        Merci pour votre inscription. Retrouvez toutes les informations concernant votre inscription à l'adresse suivante:
        """
        + base_url
        + f"/#/{person}/1/{uuid}"
        + """
        L'équipe Vélobus
        """
    )
    html_message = f"<p>Bonjour</p><p>Merci pour votre inscription. Retrouvez toutes les informations concernant votre inscription par le lien suivant: <a href='{base_url}/#/{person}/1/{uuid}'>inscription</a>.</p><p>Cordialement<br>L'équipe Vélobus</p>"

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


class ResponsibleViewSet(ModelViewSet):
    queryset = models.ResponsibleModel.objects.all()
    serializer_class = serializers.ResponsibleSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        send_welcome_mail("responsible", instance.uuid, instance.email)


class StudentViewSet(ModelViewSet):
    queryset = models.StudentModel.objects.all()
    serializer_class = serializers.StudentSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        send_welcome_mail("student", instance.uuid, instance.email)
