# Movie playlist website

- The application has user authentication ( Sign In/ Sign Up )
- After logging in users will be navigated to the home screen where they  search option where t they can search movies and see details of those movies.  
- They can create a list of movies by adding the movies to lists.
On the public page, different movie lists created by that user will be displayed. 
- These lists can be either public ( anyone with a link to the list can see this ) or private ( only the person who created can see this list ).
## .env file
DJANGO_KEY= django-secret-key\
OMDB_API_KEY= your-omdbapi-key\
get OMDB API-KEY from https://www.omdbapi.com/apikey.aspx
## Usage
```
cd <project-directory>
```
```
pip install -r requirements.txt
```
```
python manage.py runserver
```
```
python manage.py runserver
```
## Docker Build command
```
docker build --build-arg DJANGO_KEY=django-secret --build-arg OMDB_API_KEY=omdbapi-key -t movie_playlist  .
```
## Application Deployed in a Linux server
Deployed here [link](http://194.195.118.196/) 
