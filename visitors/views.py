from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, View, DeleteView
from django.contrib.auth.views import LoginView
from .models import User, Profile, RoomType, Booking, Room, Review, GetContact
from .forms import SignupForm, MyAuthenticationForm, BookingForm, ReviewForm, GetContactForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import UserPassesTestMixin
from datetime import datetime
from django.db.models import Q
from staff.forms import BookingForm2
from django.contrib import messages



# Create your views here.


def homepage(request):
    return render(request, 'homepage.html')


class Signup(CreateView):
    model = User
    form_class = SignupForm
    success_url = reverse_lazy('update_profile')
    template_name = 'accounts/signup.html'
    extra_context = {'item_type': 'User', 'form_type': 'Create'}

    def form_valid(self, form):
        self.object = form.save()
        user = authenticate(self.request, username=self.object.username, password=form.cleaned_data['password1'])
        if user:
            login(self.request, user)
        return HttpResponseRedirect(self.get_success_url())


class UpdateProfile(UpdateView):
    model = Profile
    fields = ['phone', 'address']
    success_url = reverse_lazy('homepage')
    template_name = 'partials/create.html'
    extra_context = {'item_type': 'Profile', 'form_type': 'Update'}

    def get_object(self, queryset=None):
        return self.request.user.profile


class MyLoginView(LoginView):
    template_name = 'accounts/login.html'
    form_class = MyAuthenticationForm


class ViewProfile(DetailView):
    model = User
    template_name = 'accounts/profile.html'
    context = Booking


class RoomTypeListView(ListView):
    model = RoomType
    template_name = 'room_detail.html'
    context_object_name = 'roomstype'


class BookingCreateView(LoginRequiredMixin, CreateView):
    template_name = 'booking.html'
    success_url = reverse_lazy('homepage')
    model = Booking
    form_class = BookingForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        start = form.cleaned_data['start_date']
        end = form.cleaned_data['end_date']
        room = form.cleaned_data['room']
        number_people = form.cleaned_data['number_people']

        not_available = Booking.objects.filter(Q(start_date__lte=start, end_date__gte=end) | Q(start_date__lte=end, end_date__gte=end) | Q(start_date__gte=start, end_date__lte=end) | Q(end_date__gte=start, end_date__lte=end))
        avail_rooms = Room.objects.exclude(booking__in=not_available)
        if room in avail_rooms:
            if number_people < (room.room_type.max_people + 1):
                self.object.user = self.request.user
                self.object = form.save()
                return render(self.request, 'confirmation.html')
            else:
                return render(self.request, 'too_many.html', {'room':room})
        else:
            return render(self.request, 'unvailable_rooms.html')



class ReviewCreateView(LoginRequiredMixin, CreateView):
    template_name = 'new_review.html'
    success_url = reverse_lazy('homepage')
    model = Review
    form_class = ReviewForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

class GetContactCreateView(CreateView):
    template_name = 'new_request.html'
    model = GetContact
    form_class = GetContactForm

    def form_valid(self, form):
        self.object = form.save()
        return render(self.request, 'request_success.html')

@staff_member_required
def booking_view(request):
    current_month = datetime.now().month
    return render(request,'allbooking.html', {'booking':Booking.objects.filter(Q(start_date__month=current_month) | Q(end_date__month=current_month))})

@staff_member_required
def single_booking(request, book_id):
    return render(request, 'single_booking.html',{'single_book': Booking.objects.get(id=book_id)})


class StaffBookingCreateView(UserPassesTestMixin,CreateView):
    template_name = 'partials/create.html'
    success_url = reverse_lazy('list_bookings')
    model = Booking
    form_class = BookingForm2

    def test_func(self):
        return self.request.user.is_staff

    def form_valid(self, form):
        self.object = form.save(commit=False)
        start = form.cleaned_data['start_date']
        end = form.cleaned_data['end_date']
        room = form.cleaned_data['room']
        number_people = form.cleaned_data['number_people']

        not_available = Booking.objects.filter(Q(start_date__lte=start, end_date__gte=end) | Q(start_date__lte=end, end_date__gte=end) | Q(start_date__gte=start, end_date__lte=end) | Q(end_date__gte=start, end_date__lte=end))
        avail_rooms = Room.objects.exclude(booking__in=not_available)
        if room in avail_rooms:
            if number_people < (room.room_type.max_people + 1):
                self.object = form.save()
                return HttpResponseRedirect(self.get_success_url())
            else:
                return render(self.request, 'too_many.html', {'room':room})
        else:
            return render(self.request, 'unvailable_rooms.html')


class ListRequest(ListView,UserPassesTestMixin):
    model = GetContact
    template_name = 'requests_list.html'
    context_object_name = 'requests'

    def test_func(self):
        return self.request.user.is_staff

class BookingUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'partials/create.html'
    model = Booking
    form_class = BookingForm2
    success_url = reverse_lazy('list_bookings')

    def form_valid(self, form):
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def test_func(self):
        return self.request.user.is_staff


class BookingDeleteView(UserPassesTestMixin, DeleteView):
    model = Booking
    template_name = 'delete_view.html'
    success_url = reverse_lazy('list_bookings')
    success_message = "The reservation was deleted successfully"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message  % obj.__dict__)
        return super(BookingDeleteView, self).delete(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staff

class ListReview(ListView):
    model = Review
    template_name = 'reviews_list.html'
    context_object_name = 'reviews'

class DeleteReview(DeleteView, UserPassesTestMixin):
    model = Review
    template_name = 'delete_view.html'
    success_url = reverse_lazy('list_bookings')
    success_message = "The review was deleted successfully"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message % obj.__dict__)
        return super(DeleteReview, self).delete(request, *args, **kwargs)

    def test_func(self):
        return self.request.user.is_staff
