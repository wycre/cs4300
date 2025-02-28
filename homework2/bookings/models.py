from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    duration = models.IntegerField()

    def __str__(self):
        return self.title

class Seat(models.Model):
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return self.seat_number

class Booking(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.booking_date = datetime.today()