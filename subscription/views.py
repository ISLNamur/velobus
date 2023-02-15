import uuid
import requests

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet, GenericViewSet
from rest_framework import mixins
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.conf import settings
from django.http import HttpResponse

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
            for contact in models.ResponsibleModel.objects.filter(
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
        + "Dès que votre inscription est validée et votre mot de passe généré, retrouvez les inscriptions à l'adresse suivante :"
        if person == "responsible"
        else "" + f"{base_url}/#/list"
        if person == "responsible"
        else ""
        + """
        L'équipe Vélobus
        """
    )
    html_message = (
        """<p>Bonjour</p><p>Merci pour votre inscription. Retrouvez toutes les informations concernant votre inscription par le lien suivant:
    """
        + f" <a href='{base_url}/#/{person}/4/{uuid}'>inscription</a>."
        + f"Vous pouvez également y changer vos dates de parcours.<br>{'<br>'.join(contacts)}</p>"
        + "<p>Dès que votre inscription est validée et votre mot de passe généré, retrouvez les inscriptions à l'adresse suivante :"
        if person == "responsible"
        else "" + f"<a href='{base_url}/#/list'>{base_url}/#/list</a></p>"
        if person == "responsible"
        else "" + "<p>Cordialement<br>L'équipe Vélobus</p>"
    )

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
        user = User.objects.create_user(instance.email, instance.email, uuid.uuid4())
        instance.user = user
        instance.save()
        send_welcome_mail("responsible", instance.uuid, instance.email)


class ValidateAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, uuid, format=None):
        response = HttpResponse()
        try:
            responsible = models.ResponsibleModel.objects.get(uuid=uuid)
            responsible.validated = True
            responsible.save()
        except ObjectDoesNotExist:
            response.status_code = 404
            return response

        domain = (
            f"{settings.ALLOWED_HOSTS[0]}" if settings.ALLOWED_HOSTS else "127.0.0.1:8000"
        )

        url = f"http{'' if settings.DEBUG else 's'}://{domain}/accounts/password_reset/"

        client = requests.session()
        client.get(url)
        csrftoken = client.cookies["csrftoken"]
        data = {
            "email": responsible.email,
            "csrfmiddlewaretoken": csrftoken,
        }

        cookies = dict(client.cookies)
        requests.post(
            url,
            data=data,
            headers={"HTTP_HOST": domain, "X-CSRFToken": csrftoken},
            cookies=cookies,
        )

        response.status_code = 201
        return response


class ResponsibleListView(ReadOnlyModelViewSet):
    queryset = models.ResponsibleModel.objects.all()
    serializer_class = serializers.ResponsibleDepthSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["track", "subscription__subscription_date"]


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
    queryset = models.StudentModel.objects.all()
    serializer_class = serializers.StudentDepthSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["track", "subscription__subscription_date"]
