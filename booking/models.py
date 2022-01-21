# from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)

# Create your models here.

# class Custom_manager(BaseUserManager):
#     def create_superuser(self, user_name, password, **other_fields):
#         other_fields.setdefault("is_superuser", True)

#         if other_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must be assigned to is_superuser = True.")

#         return self.create_user(user_name, password, **other_fields)

#     def create_user(self, user_name, password, **other_fields):

#         if not user_name:
#             raise ValueError("you must provide an phone")
#         user = self.model(user_name=user_name, **other_fields)

#         # user.set_password(validated_data['password'])
#         user.set_password(password)
#         user.save()
#         return user


class Users(models.Model):
    user_name = models.CharField(max_length=10, unique=True, primary_key=True)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=160000)
    otp = models.CharField(max_length=4)
    user_level = models.IntegerField(default=2)
    verified = models.BooleanField(default=False)
    # is_staff = models.BooleanField(default=False)
    # is_active = models.BooleanField(default=True)

    # objects = Custom_manager()

    # USERNAME_FIELD = "user_name"
    # REQUIRED_FIELD = ["password","first_name","last_name","email","phone"]

    def __str__(self):
        return self.user_name

class Movies(models.Model):
    user_name = models.ForeignKey(Users, on_delete=models.CASCADE)
    movie_name = models.CharField(max_length=300, primary_key=True, unique=True)
    seats = models.IntegerField()
    price = models.IntegerField()
    genre = models.CharField(max_length=20)
    description = models.CharField(max_length=500)

    def __str__(self):
        return self.movie_name



