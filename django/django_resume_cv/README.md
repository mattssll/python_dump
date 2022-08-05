# Django Resume Website
This is a front-end website built with html/css, rendered on Django, and deployed to Heroku.
## Check the App (my cv) here: https://mattssll.herokuapp.com/


### This is the Tech. Stack used here:
<img src="techstack.png">


We'll be using Python and Virtualenv to start with it.<br>
<h4>Some steps to build and deploy it:</h4>
<h4>Credits on the Django/Heroku deployment and full tutorial for doubts here: <a href='https://www.youtube.com/watch?v=F5WXNI3Dq8U&t=535s'> <a></h4>
<ul>
    <li>First install Python in your computer, then run on terminal "pip install virtualenv"</li>
    <li>Create a virtual env with "python -m venv venv" in the terminal, in the folder you're building the app, terminal code might be slightly different with linux/windows</li>
    <li>To activate the venv: 
    In linux: source vnenv/Scripts/activate
    In windows: venv\Scripts\activate</li>
    <li>Install django with "pip install django" in the terminal with the venv env.</li>
    <li>Create Django Project, in the terminal: django-admin.py startproject djangoresume</li>
    <li>Migrate "db": 
linux:winpty python manage.py migrate
windows python manage.py migrate</li>
    <li>run server: python manage.py runserver, django should be running now on localhost:8000</li>
    <li>Start our app with Django, create our app folder: python manage.py startapp resumewebsite</li>
    <li>Create a new file called urls.py</li>
    <li>Get content from urls.py in folder djangoresume and copy inside urls.py in resumewebsite, in the original 
urls.py - need to add include in from django.urls import path, include and also in url patterns, after the first path, put a comma and add "path('', include('resumewebsite.urls'))</li>
    <li>in settings.py, need to add "'resumewebsite'" as an item in INSTALLED_APPS</li>
    <li>In resumesite create a new folder called templates, and inside templates let's put our template inside this folder, let's also create a folder called static with a folder called css and a folder called images, and let's put the css and the image from the template there</li>
    <li>
In views.py create a view for the home page</li>
    <li>Deployment: Create some SSH Keys to connect to Heroku with our terminal:
mkdir .ssh
cd .ssh
ssh-keygen.exe (in linux and windows)
heroku login
heroku keys:add</li>
    <li>modify our app before pushing it to heroku (create a file called "Procfile" in \djangoresume\djangoresume)</li>
    <li>add to the Procfile: "web: gunicorn djangoresume.wsgi", without the quotes</li>
    <li>then install some things that Heroku is gonna need, go to settings.py,
pip install django_heroku
pip install python-decouple
pip install dj_database_url</li>
    <li>Add to our settings.py:
import dj_database_url
from decouple import config
import django_heroku</li>
    <li>in middleware in settings.py first and second line should be:
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',...
</li>
    <li>add in the end of our settings.py
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
django_heroku.settings(locals())</li>
    <li>in terminal, to create requirements file: pip freeze > requirements.txt</li>
    <li>in terminal type "heroku create appname" to create a new app </li>
    <li>then git push heroku master to push the git repo we created to heroku</li>
</ul>





















