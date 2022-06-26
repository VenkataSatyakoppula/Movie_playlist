from django.contrib import admin
from django.urls import path
from .views import Login,Home,Register,Playlists,logout_view,specific_playlist,delete_playlist,Add_to_playlist,Movie_view,delete_movie,Public_playlist
from .views import make_public,Profile_view,change_password,delete_user

urlpatterns = [
    path('', Home.as_view(),name='home'),
    path('accounts/login/', Login.as_view(),name='login'),
    path('register',Register.as_view(),name='register'),
    path('logout', logout_view,name='logout'),
    path('change_password',change_password,name='change_password'),
    path('delete',delete_user,name='delete_user'),
    path("profile", Profile_view.as_view(), name="profile"),
    path('playlist',Playlists.as_view(),name='playlist'),
    path('specific/<int:pk>',specific_playlist.as_view(),name='specific'),
    path('specific/delete/<int:pk>',delete_playlist,name='delete_specific'),
    path('specific/add/<str:id>/<int:id2>/<str:name>',Add_to_playlist.as_view(),name='add_to_playist'),
    path('specific/movie_view/<str:id>',Movie_view.as_view(),name='movie_view'),
    path('specific/movie_delete/<int:playlist_id>/<int:pk>',delete_movie,name='movie_delete'),
    path('playlist/public',Public_playlist.as_view(),name='public_playlist'),
    path('playlist/make_public/<int:pk>',make_public,name='make_public')
]
