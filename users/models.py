
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models
from django_countries.fields import CountryField
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser)


class CustomUser(AbstractUser):
    pass

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.is_admin = False
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self.db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address', 
        max_length=255,
        unique=True,
    )
    is_student = models.BooleanField(default=False) 
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default =False)
    is_staff = models.BooleanField(default=True)


    USERNAME_FIELD='email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        "Does the user have a specific permission"
        return True

    def has_module_perms(self,app_label):
        "Does the user have permissions to view the app 'app_label'?"
        return True

class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # detail
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    preferred_name = models.CharField(max_length=100)
    current_job_title = models.CharField(max_length=255)
    website = models.CharField(max_length=255)

    # log ins
    discord_name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="media/profile-images")
    github_username = models.CharField(max_length = 100)
    codepen_username = models.CharField(max_length=100)
    fcc_profile_url = models.CharField(max_length=255)
    LEVELS = (
        (1, 'Level One'),
        (2, 'Level Two'),
    )
    current_level = models.IntegerField(choices=LEVELS)
    phone = models.CharField(max_length=50)

    #  Location
    timezone = models.CharField(max_length=50)
    country = CountryField(multiple=False),
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'