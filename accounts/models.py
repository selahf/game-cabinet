from django.db import models
from django.contrib.auth.models import AbstractBaseUser


class MyUser(AbstractBaseUser):
    identifier = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    bio = models.CharField(blank=True, max_length=300)
    birthday = models.DateField()
    profileImage = models.ImageField(blank=True)
    joinDate = models.DateField()

    USERNAME_FIELD = "identifier"
    REQUIRED_FIELDS = ["identifier", "name"]

    def __str__(self):
        return self.name
