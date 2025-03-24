from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', False)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    class DocEnum(models.TextChoices):
        OPTION1 = "true"
        OPTION2 = "false"

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=15)
    password = models.CharField(max_length=100)
    file_status = models.CharField(max_length=10, choices=DocEnum.choices, default=DocEnum.OPTION2)
    video_status = models.CharField(max_length=10, choices=DocEnum.choices, default=DocEnum.OPTION2)
    file_path = models.CharField(max_length=500, default="null")
    video_path = models.CharField(max_length=100, default="null")
    date_time = models.DateTimeField(default=timezone.now)
    deleted = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    dob = models.DateField(null=True)
    profile_image = models.CharField(max_length=100,null=True, blank=True)
    google_id = models.CharField(max_length=100, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username', 'mobile']

    def __str__(self):
        return self.email





    