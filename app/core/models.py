from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_field):
        if not email:
            raise ValueError("User must have an email")
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Tag(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Ingredient(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name



class Recipe(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=200)
    time_minute = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    descripcion = models.TextField(blank=True)
    link = models.CharField(blank=True, max_length=200)
    tags = models.ManyToManyField('Tag')
    ingredients= models.ManyToManyField('Ingredient')

    def __str__(self):
        return self.title
