from django.db import models
from django.contrib.auth.models import User
import os
# Create your models here.
class tutor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=75)
    mobno = models.CharField(max_length=10,null=True,default=0)
    subject = models.CharField(max_length=100,null=True)
    price = models.IntegerField(default=0)
    hours = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    image = models.URLField()
    days = models.IntegerField(default=0)

class school(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=75)
    mobno = models.CharField(max_length=10,null=True,default=0)
    board = models.CharField(max_length=200)
    website = models.URLField(max_length=200)
    tillclass = models.IntegerField(default=0)
    medium = models.CharField(max_length=100)
    fees = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    image = models.URLField()
    location = models.CharField(max_length=200)

class books(models.Model):
    bookname = models.CharField(max_length=100)
    sellername = models.CharField(max_length=100)
    sellerno = models.CharField(max_length=10,null=True,default=0)
    selleremail = models.EmailField(max_length=75)
    sellprice = models.IntegerField(default=0)
    orgprice = models.IntegerField(default=0)
    image = models.URLField()
    quantity = models.IntegerField(default=1)
    overview = models.CharField(max_length=200)

class spaces(models.Model):
    location = models.CharField(max_length=200)
    rooms = models.IntegerField(default=1)
    equip = models.CharField(max_length=200)
    hours = models.IntegerField(default=1)
    charge = models.IntegerField(default=0)
    sellername = models.CharField(max_length=100)
    sellerno = models.CharField(max_length=10,null=True,default=0)
    selleremail = models.EmailField(max_length=75)
    image = models.URLField()

class contact(models.Model):
    name = models.CharField(max_length=75)
    email = models.EmailField(max_length=75)
    mobno = models.CharField(max_length=10,null=True,default=0)
    message = models.CharField(max_length=300)

class institute(models.Model):
    name = models.CharField(max_length=75)
    email = models.EmailField(max_length=100)
    location = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    courses = models.CharField(max_length=200)
    years = models.IntegerField(default=0)
    enroll = models.IntegerField(default=0)
    foundername = models.CharField(max_length=75)
    mobno = models.CharField(max_length=10,null=True,default=0)
    website = models.URLField(max_length=200)
    staff = models.IntegerField(default=1)
    image = models.URLField()
    count = models.IntegerField(default=0)

class extuser(models.Model):
    email = models.EmailField(max_length=40)
    is_student = models.BooleanField(default=False)
    is_school = models.BooleanField(default=False)
    is_institute = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    is_owner = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_college = models.BooleanField(default=False)

def get_image_path(instance, filename):
    return os.path.join('photos', str(instance.course_id), filename)

class courses(models.Model):
    name = models.CharField(max_length=100)
    overview = models.CharField(max_length=200)
    image = models.ImageField(upload_to=get_image_path, blank=True, null=True)
    email = models.EmailField(max_length=75)
    tchrname = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    price = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    course_id = models.IntegerField(default=0)
    COURSE_CHOICES = (
        ('Online', 'Online'),
        ('Offline', 'Offline'),
        ('Both', 'Both'),
    )
    course_mode = models.CharField(max_length=7, choices=COURSE_CHOICES)

def get_video_path(instance, filename):
    return os.path.join('videos', str(instance.course_id), filename)

class epcourse(models.Model):
    course_id = models.IntegerField(default=0)
    video = models.FileField(upload_to=get_video_path)
    ep_overview = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'epcourse'
        verbose_name_plural = 'epcourse'
         

class enroll(models.Model):
    course_id = models.IntegerField(default=0)
    email = models.EmailField(max_length=75)

class enrollcontact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=75)
    mobno = models.CharField(max_length=10,null=True,default=0)
    coursename = models.CharField(max_length=100)
    
class college(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=75)
    mobno = models.CharField(max_length=10,null=True,default=0)
    major = models.CharField(max_length=200)
    website = models.URLField(max_length=200)
    fees = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    image = models.URLField()
    location = models.CharField(max_length=200)
