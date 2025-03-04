import random
import string
from django.contrib.auth.models import BaseUserManager

# Custom User Manager
class UserManager(BaseUserManager):
   
    def create_user(self, email, user_type, full_name, password=None, password2=None):
        """
        Creates and saves a User with the given email, user_type, and password.
        """
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            user_type=user_type,
            full_name=full_name
        )

        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, full_name='Admin user', user_type='Admin', password=None):
        """
        Creates and saves a superuser with the given email, full_name, and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            user_type=user_type,
            full_name=full_name
        )
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user