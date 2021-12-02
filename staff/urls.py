from django.urls import path
from visitors.urls import views
from visitors.views import booking_view, single_booking, StaffBookingCreateView, ListRequest, BookingUpdateView, BookingDeleteView,ListReview


urlpatterns = [
    path('bookings', views.booking_view, name='list_bookings'),
    path('bookings/<int:book_id>', views.single_booking, name='single_book'),
    path('makeBooking/', views.StaffBookingCreateView.as_view(), name='make_booking'),
    path('infoRequest/', views.ListRequest.as_view(), name='list_request'),
    path('updateBooking/<int:pk>/', views.BookingUpdateView.as_view(), name='update_booking'),
    path('<int:pk>/deleteBooking/', views.BookingDeleteView.as_view(), name='delete'),
    path('reviews/', views.ListReview.as_view(), name='all_reviews'),
    path('<int:pk>/deleteReview/', views.DeleteReview.as_view(), name='delete_reviews'),

    ]