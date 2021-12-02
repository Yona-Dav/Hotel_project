from django.contrib import admin

# Register your models here.

from visitors.models import Profile, Room, RoomType, Booking, Review, GetContact
admin.site.register(Profile)
admin.site.register(Room)
admin.site.register(RoomType)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(GetContact)

