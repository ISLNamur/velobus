import uuid
from django.db import models
from django.contrib.auth.models import User


class TrackModel(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=10)
    track_coordinates = models.JSONField()

    def __str__(self):
        return self.name


class StopModel(models.Model):
    name = models.CharField(max_length=200)
    track = models.ForeignKey(TrackModel, on_delete=models.CASCADE)
    time_morning = models.TimeField(blank=True, null=True)
    time_afternoon = models.TimeField(blank=True, null=True)
    place = models.CharField(max_length=500)
    picture = models.ImageField(upload_to="places", blank=True, null=True)
    coordinates = models.JSONField()

    def __str__(self):
        return f"{self.name} ({self.track})"


class SchoolModel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class AvailableDateModel(models.Model):
    date = models.DateField()

    def __str__(self):
        return str(self.date)


class DateSubscriptionModel(models.Model):
    subscription_date = models.ForeignKey(AvailableDateModel, on_delete=models.CASCADE)
    morning = models.BooleanField(default=False)
    afternoon = models.BooleanField(default=False)
    comment = models.TextField(blank=True)
    datetime_creation = models.DateTimeField(auto_now_add=True)
    datetime_modification = models.DateTimeField(auto_now=True)


class PersonModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    school = models.ForeignKey(SchoolModel, on_delete=models.CASCADE)
    email = models.EmailField()
    subscription = models.ManyToManyField(DateSubscriptionModel, blank=True)
    track = models.ForeignKey(
        TrackModel, on_delete=models.SET_NULL, null=True, blank=True
    )
    stop = models.ForeignKey(StopModel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        abstract = True


class ResponsibleModel(PersonModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    is_point_of_contact = models.BooleanField(default=False)


class StudentModel(PersonModel):
    classe = models.CharField(max_length=20)
    street = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    locality = models.CharField(max_length=40)
    student_phone = models.CharField(max_length=20, blank=True)
