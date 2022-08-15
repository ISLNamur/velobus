from urllib.parse import MAX_CACHE_SIZE
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
    time_morning = models.TimeField()
    time_afternoon = models.TimeField()
    place = models.CharField(max_length=500)
    picture = models.ImageField(upload_to="places")
    coordinates = models.JSONField()


class SchoolModel(models.Model):
    name = models.CharField(max_length=100)


class AvailableDateModel(models.Model):
    date = models.DateField()


class DateSubscriptionModel(models.Model):
    subscription_date = models.ForeignKey(AvailableDateModel, on_delete=models.CASCADE)
    morning = models.BooleanField()
    afternoon = models.BooleanField()
    comment = models.TextField(blank=True)
    datetime_creation = models.DateTimeField(auto_now_add=True)
    datetime_modification = models.DateTimeField(auto_now=True)


class PersonModel(models.Model):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20, blank=True)
    school = models.ForeignKey(SchoolModel, on_delete=models.CASCADE)
    email = models.EmailField()
    subscription = models.ManyToManyField(DateSubscriptionModel, blank=True)

    class Meta:
        abstract = True


class ResponsibleModel(PersonModel):
    track = models.ForeignKey(
        TrackModel, on_delete=models.SET_NULL, null=True, blank=True
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class StudentModel(PersonModel):
    uuid = models.UUIDField(primary_key=True)
    street = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    locality = models.CharField(max_length=40)
    student_phone = models.CharField(max_length=20, blank=True)
