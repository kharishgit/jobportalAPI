from django.conf import settings
from django.db import models
from account.models import User
# Create your models here.
class company(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True)
    company_name = models.CharField(max_length=100,null=True)
    website = models.URLField(max_length=200,null=True)
    size = models.CharField(max_length=20,null=True, blank=True)
    founded = models.CharField(max_length=10,null=True, blank=True)
    stage = models.CharField(max_length=20,null=True, blank=True)
    about = models.TextField(null=True)
    linked_in = models.URLField(max_length=200,null=True, blank=True)



