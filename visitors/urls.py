from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),
    path('signup/', views.Signup.as_view(), name='signup'),
    path('profile/update/', views.UpdateProfile.as_view(), name='update_profile'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/<int:pk>/', views.ViewProfile.as_view(), name='profile'),
    path('booking/viewRooms/',views.RoomTypeListView.as_view(), name='details_room_type'),
    path('booking/', views.BookingCreateView.as_view(), name='booking'),
    path('review/',views.ReviewCreateView.as_view(), name='review'),
    path('getContact/',views.GetContactCreateView.as_view(), name='contact'),



]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)