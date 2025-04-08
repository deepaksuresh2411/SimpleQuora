from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class AppUserManager(UserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email Field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class AppUser(AbstractUser):
    username = None
    email = models.EmailField(
        verbose_name="Email ID", blank=True, unique=True
    )
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email
    
    objects = AppUserManager()
    