from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Booking, Review, GetContact


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class MyAuthenticationForm(AuthenticationForm):
    fields = ['username','password']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        exclude = ['user']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['title','message']

class GetContactForm(forms.ModelForm):
    class Meta:
        model = GetContact
        fields = '__all__'