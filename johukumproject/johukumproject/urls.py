"""
URL configuration for johukumproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from johukumapp.views import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('service/', ServiceView.as_view()),
    path ('service/<pk>/',ServiceView.as_view()),
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view(), name="register"),
    path('register/<int:pk>', RegisterView.as_view(), name='register'),
    path('bookings/', BookingCreateView.as_view(), name='create-booking'),
    path('bookings/<booking_id>', BookingCreateView.as_view(), name='create-booking'),
    path('confirm-booking/', ConfirmBookingView.as_view(), name='confirm-booking'),
   path('user-search/<int:pk>', SearchUserByService.as_view(), name='confirm-booking'),

    # path('api/bookings/', BookingAPIView.as_view(), name='booking_api'),
    # path('api/confirm-booking/', ConfirmBookingAPIView.as_view(), name='confirm_booking_api'),
]
