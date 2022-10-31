from datetime import datetime
from django.conf import settings
import email
from turtle import title
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.gis.db import models as gismodels
from django.contrib.gis.geos import Point
from django.contrib.auth.models import User
import geocoder
import os
from datetime import timedelta



# Create your models here.

class jobType(models.TextChoices):
    Permanent='Permanent'
    Temporary='Temporary'
    Intership='Intership'
    WFH='WFH'

class Education(models.TextChoices):
    Bachelors='Bachelors'
    Masters='Masters'
    Phd ='Phd'

class Industry(models.TextChoices):
    Buisness='Buisness'
    IT ='Information Technology'
    Education='Education&Training'
    Telecommunication='Telecommunication'
    Banking='Banking'
    Others = 'Others'

class Experience(models.TextChoices):
    NO_EXPERIENCE = 'No Experience'
    ONE_YEAR = '1 Year'
    TWO_YEAR = '2 Year'
    THREE_PLUS = '3 Years and more'

def return_date_time():
    now = datetime.now()
    return now + timedelta(days=10)


class jobs(models.Model):
    title= models.CharField(max_length=200,null=True)
    description = models.TextField(null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=100,null=True)
    jobType = models.CharField(
        max_length=10,
        choices=jobType.choices,
        default=jobType.Permanent
    )
    education = models.CharField(
        max_length=10,
        choices=Education.choices,
        default=Education.Bachelors
    )
    Industry = models.CharField(
        max_length=30,
        choices=Industry.choices,
        default=Industry.Buisness
    )
    Experience = models.CharField(
        max_length=20,
        choices=Experience.choices,
        default=Experience.NO_EXPERIENCE
    )
    salary= models.IntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(1000000)])
    positions =models.IntegerField(default=1)
    company = models.CharField(max_length=100,null=True)
    point = gismodels.PointField(default=Point(0.0,0.0))
    last_date = models.DateTimeField(default=return_date_time)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,blank=True)
    created_At = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        g=geocoder.mapquest(self.address,key=os.environ.get('GEO_CODER_API'))
        print(g)
        lng=g.lng
        lat=g.lat
        self.point=Point(lat,lng)
        super(jobs,self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class CandidatesApplied(models.Model):
    jobs = models.ForeignKey(jobs, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True)
    resume = models.CharField(max_length=200)
    appliedAt = models.DateTimeField(auto_now_add=True)

    # def skill(self):
    #     return self.user.skill

    def __str__(self):
        return self.jobs.title
