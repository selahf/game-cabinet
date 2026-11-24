from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager


class MyUserManager(BaseUserManager):

    def create_user(self, identifier, name, password=None, **extra_fields):
        if not identifier:
            raise ValueError("Users must have an identifier.")

        user = self.model(
            identifier=identifier,
            name=name,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    identifier = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    bio = models.CharField(blank=True, max_length=300)
    birthday = models.DateField(blank=True, null=True)
    profileImage = models.ImageField(blank=True)
    joinDate = models.DateField(blank=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = "identifier"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return self.name