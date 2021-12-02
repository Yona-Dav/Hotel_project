from visitors.models import Booking
from django.contrib.auth.models import User
from django import forms

class BookingForm2(forms.ModelForm):
    class Meta:
        model = Booking
        fields ='__all__'