import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hotel.settings')
django.setup()


from faker import Faker
from django.contrib.auth.models import User
import random
from visitors.models import Profile, Room, RoomType, Booking

f = Faker()

def new_user(num):
    for i in range(num):
        fname = f.first_name()
        lname = f.last_name()
        username = fname.lower() + lname.lower()
        email = f.email()
        password = f.password()
        user = User.objects.create_user(username=username, password=password, first_name=fname, last_name=lname, email=email)


# new_user(15)

def num_room():
    for i in range(100,120):
        room = Room.objects.create(room_type=RoomType.objects.get(id=1), room_number=i)
    for i in range(200,215):
        room = Room.objects.create(room_type=RoomType.objects.get(id=2), room_number=i)
    for i in range(300,312):
        room = Room.objects.create(room_type=RoomType.objects.get(id=3), room_number=i)
    for i in range(400,410):
        room = Room.objects.create(room_type=RoomType.objects.get(id=4), room_number=i)
    for i in range(500,505):
        room = Room.objects.create(room_type=RoomType.objects.get(id=6), room_number=i)
    for i in range(600,603):
        room = Room.objects.create(room_type=RoomType.objects.get(id=5), room_number=i)
    room = Room.objects.create(room_type=RoomType.objects.get(id=7), room_number=700)

# num_room()

def available_rooms(start, end):
    not_available1 = Booking.objects.filter(start_date__lt=start, end_date__gt=end)
    not_available2 = Booking.objects.filter(start_date__lt=end, end_date__gt=end)
    not_available3 = Booking.objects.filter(start_date__gt=start, end_date__lt=end)
    not_available4 = Booking.objects.filter(end_date__gt=start, end_date__lt=end)

    avail_rooms = Room.objects.exclude(booking__in = not_available1).exclude(booking__in = not_available2).exclude(booking__in = not_available3).exclude(booking__in = not_available4)
    return avail_rooms


def pop_booking(num):
    for i in range(num):
        start_date = f.date_time_this_year()
        while True:
            end_date = f.date_time_this_year()
            if end_date>start_date:
                break

        room = random.choice(available_rooms(start_date, end_date))
        user = random.choice(User.objects.all())
        number = random.randint(1,room.room_type.max_people)

        book = Booking.objects.create(room=room, start_date= start_date, end_date=end_date, user=user, number_people=number)


# pop_booking(40)