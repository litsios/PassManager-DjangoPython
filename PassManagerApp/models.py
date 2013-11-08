from django.db import models
from django.contrib.auth.models import User
class UserProfile(models.Model):
    #required by the auth model, creates the user
    #using unique because username is our primary key for the database
    user = models.ForeignKey(User, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
class login(models.Model):
    #details to be saved for a login entry
    name = models.CharField(max_length=200)
    loginUrl = models.CharField(max_length=200)
    password = models.CharField(max_length=100)
    username = models.ForeignKey(User)
    login_username = models.CharField(max_length=200)
    #saves the current datetime
    date = models.DateField(auto_now=True)
    notes = models.TextField()
