from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = PhoneNumberField(blank=True)
    address = models.TextField(null=True)


class RoomType(models.Model):
    name = models.CharField(max_length=50)
    max_people = models.IntegerField()
    cost = models.IntegerField()
    details = models.TextField(null=True)
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Room(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE)
    room_number = models.IntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_number} : {self.room_type}"


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_people = models.IntegerField()

    def __str__(self):
        return f"{self.room} booked by {self.user}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateField(auto_now_add=True)

class GetContact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    request = models.TextField()






