from rest_framework import serializers
from .models import *
from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .managers import UserManager
User = get_user_model()

from rest_framework import serializers
from .models import User  # Import your User model

# ankit start
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Service
        fields='__all__'
# ankit end

# richa start
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Service
        fields='__all__'
class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)  # Add password2 field
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        """Ensure that password and password2 match."""
        password = data.get("password")
        password2 = data.pop("password2", None)  # Remove password2 from validated data
        
        if password and password2 and password != password2:
            raise serializers.ValidationError({"password2": "Passwords do not match."})

        return data

    def create(self, validated_data):
        """Create a new user with a hashed password."""
        password = validated_data.pop("password", None)
        user = User(**validated_data)
        
        if password:
            user.set_password(password)  # Hash the password before saving
        user.save()
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = User.objects.filter(email=data["email"]).first()
        if user and user.check_password(data["password"]):
            refresh = RefreshToken.for_user(user)
            return {
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,  # Corrected from "username"
                    "email": user.email,
                    "referral_code": user.referral_code,
                },
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        raise serializers.ValidationError("Invalid credentials")
# richa end

class BookingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookingSlot
        fields = '__all__'

class ConfirmBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmBooking
        fields = '__all__'



from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User, Service

class User1Serializer(serializers.ModelSerializer):
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        many=True
    )

    class Meta:
        model = User
        fields = ['full_name', 'email', 'mobile_no', 'user_type', 'password', 'range_field', 'address', 'service_id']

    def create(self, validated_data):
        services_data = validated_data.pop('service_id', [])
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        user.service_id.set(services_data)
        return user

