# from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "ADMIN",'Admin'
        EMPLOYER ="EMPLOYER",'Employer'
        EMPLOYEE = "EMPLOYEE",'Employee'
    base_role = Role.ADMIN
    role=models.CharField(max_length=50,choices=Role.choices)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=50,unique=True)
    education = models.CharField(max_length=50)
    experience = models.CharField(max_length=50)
    skill = models.CharField(max_length=50)
    is_admin = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False,null=True,blank=True)
    is_employee = models.BooleanField(default=False,null=True,blank=True)
    is_superadmin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name','phone_number']
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)





class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="userprofile",on_delete = models.CASCADE)
    resume = models.FileField(null=True)
    phone_number = models.CharField(max_length=12, unique=True,null=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6,null=True)
    # dotp = models.CharField(max_length=6)


    # USER_NAME_FIELD = phone_number


    REQUIRED_FIELDS = []
    objects = UserManager()



@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    user = instance

    if created:
        profile = UserProfile(user=user)
        profile.save()
