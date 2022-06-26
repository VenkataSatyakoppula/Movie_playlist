from django.contrib import admin

# Register your models here.
from .models import User,Playlist,Movie
admin.site.register(User)
admin.site.register(Playlist)
admin.site.register(Movie)