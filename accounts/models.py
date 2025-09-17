from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.dispatch import receiver
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'  # tells Django what field to log in with
    REQUIRED_FIELDS = ['first_name', 'last_name']  # used when creating superuser

    email=models.EmailField(max_length=254, unique=True)
    first_name=models.CharField(max_length=50, blank=True)
    last_name=models.CharField(max_length=50, blank=True)
    is_student=models.BooleanField(default=False)
    is_recruiter=models.BooleanField(default=False)
    date_joined=models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user=models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    readiness_score=models.DecimalField(max_digits=5, decimal_places=1,blank=True,null=True)
    applications=models.IntegerField(null=True,blank=True)
    interviews=models.IntegerField(null=True,blank=True)
    offers=models.IntegerField(null=True, blank=True)
    profile_image=models.ImageField(upload_to="image/", blank=True, null=True) # need to adjust

    def __str__(self):
        return self.user.email


# @receiver(post_save, sender=CustomUser)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.userprofile.save()
