
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import JSONField

class User(AbstractUser):
    email_verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)



class Playlist(models.Model):
    playlist_name = models.CharField(max_length=100)
    user = models.ForeignKey(get_user_model(), default=1,on_delete=models.CASCADE)
    ispublic = models.BooleanField(default=False)
    def __str__(self):
        return self.playlist_name

class Movie(models.Model):
    name = models.CharField(max_length=100)
    imdb_id = models.CharField(max_length=50,default=1)
    playlist = models.ForeignKey(Playlist,default=1, on_delete=models.CASCADE)
    