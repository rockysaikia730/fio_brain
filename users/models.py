from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db.models import Q
from rest_framework import status

from .exceptions import GeneralException
from . import utils


# According to Django convention we should have thick models/serializers and thin views
# That means we need to put most of our business logic in models or serializers

class CustomUserManager(UserManager):

    def get_user_or_404(self, query, *args, **kwargs):
        try:
            if query:
                # Users will be provided with an option to either login with email or phone
                return self.model.objects.get(Q(email=query) | Q(phone=query))
            return self.model.objects(*args, **kwargs)

        except self.model.DoesNotExist:
            raise GeneralException('Could not find an account', status_code=status.HTTP_404_NOT_FOUND)

    def inspect_password(self, query, password):
        user = self.get_user_or_404(query)

        if not check_password(password, user.password):
            raise GeneralException('Incorrect password', status_code=status.HTTP_401_UNAUTHORIZED)
        return user

    def create_user(self, email=None, phone=None, full_name=None, password=None, location=None, operation_radius=None,
                    user_type=None, *args, **kwargs):
        if not phone:
            raise ValidationError('Phone is required')

        if not full_name:
            raise ValidationError('Full name is required')

        instance = self.model(email=email, phone=phone, full_name=full_name, location=location,
                              operation_radius=operation_radius
                              )

        instance.password = utils.make_password(password)
        instance.user_type = user_type.lower()
        instance.save()
        return instance

    def create_superuser(self, email=None, phone=None, full_name=None, password=None, user_type=None, *args, **kwargs):

        instance = self.create_user(email=email, phone=phone, full_name=full_name, user_type=user_type)
        instance.set_password(password)
        instance.is_staff = True
        instance.is_superuser = True
        instance.save()
        return instance


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('buyer', 'buyer'),
        ('seller', 'seller'),
        ('admin', 'admin'),
        ('service_personal', 'service_personal')
    )

    '''
    Not needed by the user but Django needs a username field I don't know why
    We will not touch the username in anyway. Since Django needs it so we will give it a default value
    which is of course of NO use
     '''
    username = models.CharField(max_length=32, default=utils.get_uuid, blank=False, null=False)
    email = models.EmailField(blank=True, null=True, unique=True, verbose_name='Email (optional)')
    phone = models.CharField(max_length=20, blank=False, null=False, unique=True)
    full_name = models.CharField(max_length=200, blank=False, null=False)
    '''
    Not required for buyers. Only for sellers and service personals. Should be made mandatory in front-end
    '''
    location = models.CharField(max_length=256, blank=True, null=True, verbose_name='Seller/Service personal location')

    # Radius till which the product/service can be delivered. Useful for filtering
    operation_radius = models.CharField(max_length=10, blank=True, null=True)

    # Only for buyers. Should be asked while checking out. Not at the time of sign up
    delivery_address = models.CharField(max_length=256, blank=True, null=True, verbose_name='Buyer location')

    user_type = models.CharField(max_length=16, blank=False, null=False, choices=USER_TYPES)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    REQUIRED_FIELDS = ['full_name', 'user_type']

    USERNAME_FIELD = 'phone'

    def __str__(self):
        return f'{self.full_name} - {self.user_type}'
