
# richa start

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .managers import UserManager

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
# ✅ User Registration API
class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = User.objects.get(email=email)  # Fetch user manually
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials!"}, status=status.HTTP_401_UNAUTHORIZED)

        if check_password(password, user.password):  # Verify password manually
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful!",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials!"}, status=status.HTTP_401_UNAUTHORIZED)
# richa end
# ankit start


class ServiceView(APIView):
    def get(self, request,pk=None):
        if pk:
            service_get=Service.objects.get(pk=pk)
            new_service=ServiceSerializer(service_get)
            return Response(new_service.data)
        else:
            service_get = Service.objects.filter(status=True)
            new_service = ServiceSerializer(service_get,many=True)
            return Response(new_service.data)
           
# start


# Create a booking
class BookingCreateView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = BookingSlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View booking details
    def get(self, request, booking_id):
        booking = get_object_or_404(BookingSlot, booking_id=booking_id)
        serializer = BookingSlotSerializer(booking)
        return Response(serializer.data)
# Confirm booking by service provider
class ConfirmBookingView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ConfirmBookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Booking confirmed successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# List all user bookings
  
    def get(self, request):
     bookings = BookingSlot.objects.filter()
    
     if not bookings.exists():
        return Response({"message": "No bookings found."}, status=status.HTTP_404_NOT_FOUND)
    
     serializer = BookingSlotSerializer(bookings, many=True)
     return Response(serializer.data, status=status.HTTP_200_OK)