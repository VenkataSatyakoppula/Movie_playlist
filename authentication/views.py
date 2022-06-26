import re
from django import views
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from .forms import Loginform,Registerform,Profileform
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from dotenv import load_dotenv
from .models import Playlist,Movie, User
from django.contrib.auth import update_session_auth_hash
import os
import json
import requests
load_dotenv()


class Home(TemplateView):
    template_name = "home.html"
    # def get(self, request, *args, **kwargs):
    #     playlist = Playlist.objects.filter()
    #     data = list(playlist.values())
    #     print(data)
    #     return render(request, 'home.html', { 'playlist':data})
    def post(self,request,*args, **kwargs):
        req = request.POST["search"]
        key = os.getenv('OMDB_API_KEY')
        regx = re.match(r"/^ev\d{7}\/\d{4}(-\d)?$|^(ch|co|ev|nm|tt)\d{7}$",str(req),re.IGNORECASE)
        if(regx is not None):
            payload = {"i":req,"apikey":key}
        else:
            payload = {"t":req,"apikey":key}
        # try:
        r = requests.get('http://www.omdbapi.com/', params=payload)
        # except requests.JSONDecodeError:
        #     return render(request, 'home.html' , {'data': 'False'})
        # r = {'Title': 'RRR', 
        # 'Year': '2022', 
        # 'Rated': 'Not Rated', 
        # 'Released': '25 Mar 2022', 
        # 'Runtime': '187 min', 
        # 'Genre': 'Action, Drama',
        # 'Director': 'S.S. Rajamouli',
        # 'Writer': 'Vijayendra Prasad, Sai Madhav Burra, Madhan Karky', 
        # 'Actors': 'Ram Charan, N.T. Rama Rao Jr., Ajay Devgn', 
        # 'Plot': "A fictitious story about two legendary revolutionaries and their journey away from home before they started fighting for their country in 1920's.",
        # 'Language': 'Telugu, English',
        # 'Country': 'India', 
        # 'Awards': 'N/A', 
        # 'Poster': 'https://m.media-amazon.com/images/M/MV5BOTA5NzQwMGMtNDRlZC00YzA4LTliMzQtNGM0NDIwYTk5Y2ZiXkEyXkFqcGdeQXVyMTIyNzY0NTMx._V1_SX300.jpg',
        # 'Ratings': [{'Source': 'Internet Movie Database', 'Value': '8.2/10'},
        # {'Source': 'Rotten Tomatoes', 'Value': '87%'},
        # {'Source': 'Metacritic', 'Value': '87/100'}],
        # 'Metascore': '87', 'imdbRating': '8.2',
        # 'imdbVotes': '71,634',
        # 'imdbID': 'tt8178634',
        # 'Type': 'movie',
        # 'DVD': 'N/A',
        # 'BoxOffice': '$11,113,000',
        # 'Production': 'N/A',
        # 'Website': 'N/A',
        # 'Response': 'True'}
        try:
            if request.user.is_authenticated:
                playlist = request.session['playlist']
                ids = [val['id'] for val in playlist]
                print(playlist)
                play = Playlist.objects.filter(pk__in=ids)
                already_present = Movie.objects.filter(name=r.json()['Title']).filter(
                playlist__in=play
                ).exists()
                
                return render(request, 'home.html' , {'data': r.json(),'playlist':playlist,'present':already_present})
            else:
                return render(request, 'home.html' , {'data': r.json()})
        except KeyError:
            return render(request, 'home.html' , {'data': {'Response':'False'}})
            


class Login(TemplateView):
    template_name = "login.html"
    def post(self,request,*args, **kwargs):
        form = Loginform(request.POST)
        if form.is_valid():
            user = authenticate(username=form.data["email"],password=form.data["password"])
            
            if user is not None:     
                login(request,user)
                #return render(request,'base.html',{'user': user})
                request.session['User'] = user.get_username()
                playlist = Playlist.objects.filter(user=User.objects.filter(username=request.session['User']).first())
                request.session['playlist'] = list(playlist.values())
                messages.success(request,"Successfully logged in!!")
                return redirect('home')
            messages.error(request,"Invalid Crednetials!!")
        return render(request, 'login.html' , {'form': form})

class Register(TemplateView):
    template_name = "register.html"
    def post(self,request,*args, **kwargs):
        form = Registerform(request.POST)
        if form.is_valid():
            User = get_user_model()
            email = form.cleaned_data["email"]
            username = form.cleaned_data["name"]
            password = form.cleaned_data["password"]
            if (str(username).isalpha() or str(username).isalnum()) and len(username)>=4:
                obj = User(email=email,username=username)
                obj.set_password(password)
                obj.save()
                request.session['User'] = username
                playlist = Playlist.objects.filter(user=User.objects.filter(username=request.session['User']).first())
                request.session['playlist'] = list(playlist.values())
                login(request,obj)
                messages.success(request,"Successfully registered!!") 
                return redirect('home')
            messages.error(request,"Enter user name at with least 4 characters")    
        return render(request, 'register.html' , {'form': form})

@method_decorator(login_required,name='dispatch')
class Profile_view(TemplateView):
    template_name = "profile.html"
    def post(self,request,*args, **kwargs):
        form = Profileform(request.POST,instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('profile')
        return render(request,'profile.html',{'form':form})    

class Movie_view(views.View):
    def get(self, request,*args, **kwargs):
        
        imdb = self.kwargs['id']
        print(imdb)
        key = os.getenv('OMDB_API_KEY')
        payload = {"i":imdb,"apikey":key}
        r = requests.get('http://www.omdbapi.com/', params=payload)
        print(r.json())
        return JsonResponse(r.json())

def logout_view(request,*args, **kwargs):
    try:
        del request.session['User']
        del request.session['playlist']
    except:
        pass
    logout(request)
    return redirect("home")


def change_password(request,*args, **kwargs):
    # username = request.session['username']
    # userobj = User.objects.get(username=username)
    form = PasswordChangeForm(user = request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(user = request.user, data = request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        return render(request, 'change_password.html', {
        'form': form
        })
    return render(request, 'change_password.html',{'form':form})

def delete_user(request,*args,**kwargs):
    if request.user.is_authenticated:
        name = request.session["User"]
        logout(request)
        user = User.objects.filter(username=name)
        user.delete()
        messages.success(request,'User '+name+' deleted')
    return redirect('home')


def delete_playlist(request,*args, **kwargs):
    id = kwargs['pk']
    record = Playlist.objects.filter(pk=id)
    if (record.first().user == request.user) and (request.user.is_authenticated):
        record.delete()
    return redirect('playlist')


def delete_movie(request,*args, **kwargs):
    
    id = kwargs['pk']
    playlist_id = kwargs['playlist_id']
    record = Movie.objects.filter(pk=id)
    if request.user == record.first().playlist.user:
        record.delete()
        return redirect('specific',pk=playlist_id)
    else:
        messages.error(request,"Access Denied")
        return redirect('home')


def make_public(request,*args,**kwargs):
    pk = kwargs['pk']
    record = Playlist.objects.filter(pk=pk).first()
    #print(record.ispublic)
    if request.user == record.user:
        if record.ispublic:
            record.ispublic = False
        else:
            record.ispublic = True
        record.save()
        return HttpResponse(json.dumps(str(record.ispublic)+","+str(pk)),content_type="application/json")
    else:
        messages.error(request,"Access Denied")
        return redirect('home')

class specific_playlist(views.View):
    def get(self, request,*args, **kwargs):
        pk = self.kwargs['pk']
        playlist = Playlist.objects.filter(pk=pk).first()
        flag=False
        movies = Movie.objects.filter(playlist = playlist) 
        data = list(movies.values())
        if (playlist.user == request.user):         
            flag = True    
        else:
            if not playlist.ispublic: 
                messages.error(request,"Access Denied")
                return redirect('home')
        return render(request,'specific_playlist.html',{'movies':data,'playlist':playlist,'flag':flag})
        #print(data)
        # if(len(data)>0):
        #     for value in data:
        #         payload = {"i":value,"apikey":key}
        #         r = requests.get('http://www.omdbapi.com/', params=payload)
        
    
@method_decorator(login_required,name='dispatch')
class Add_to_playlist(views.View):
    # def get(self, request,*args, **kwargs):

    def get(self,request,*args, **kwargs):
        imdb = self.kwargs['id']
        playlist_id = self.kwargs['id2']
        name = self.kwargs['name']
        pl = Playlist.objects.filter(pk=playlist_id).first()
        if(request.user == pl.user):
            mv = Movie(name=name,imdb_id=imdb,playlist=pl)
            mv.save()
            messages.success(request,"Successfully added")
            return redirect('specific',pk=playlist_id)
        else:
            messages.error(request,"Access Denied")
            return redirect('home')

@method_decorator(login_required,name='dispatch')
class Playlists(views.View):
    def get(self, request, *args, **kwargs):  
            user = request.user
            print(user)
            p = Playlist.objects.filter(user = user)
            request.session['playlist'] =  list(Playlist.objects.filter(user=User.objects.filter(username=request.session['User']).first()).values())
            data = request.session['playlist']
            print(data)
            return render(request,'playlist.html',{'data':data})
    def post(self,request,*args, **kwargs):
            name = request.POST['playlist']
            user = request.user
            new_playlist = Playlist(playlist_name=name,user=user)
            new_playlist.save()
            return redirect('playlist')

class Public_playlist(views.View):
    def get(self, request, *args, **kwargs):
        p = Playlist.objects.filter(ispublic=True)
        return render(request,'public_list.html',{'public_data':p})
