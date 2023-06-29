from distutils.command.upload import upload
from email.policy import default
from this import d
from django.db import models

class Movie(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')
    year = models.CharField(max_length=5,blank=True)
    description = models.TextField(blank=True)
    time = models.CharField(max_length=20,blank=True)
    trailer = models.FileField(upload_to='trailers/',null=True)

    def __str__(self):
        return self.name

class UpcomingMovie(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name

class User(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200,blank=True)
    last_name = models.CharField(max_length=200,blank=True)
    email = models.EmailField(max_length=200,blank=True)
    
    def __str__(self):
        return self.username

class BookedSeat(models.Model):
    seat = models.IntegerField()
    userId = models.IntegerField()
    movieId = models.IntegerField()

class RazorpayPayment(models.Model):
    name = models.CharField(max_length=100)
    amount = models.IntegerField(default=100)
    provider_order_id = models.CharField(max_length=100)
 