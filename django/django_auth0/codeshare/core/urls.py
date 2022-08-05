from django.urls import path, include
from .views import PostListView, index, logout
urlpatterns = [
    path("", index), # check if user is authenticated
    path("codes", PostListView.as_view()), # our app
    path("logout", logout), 
    path("", include("django.contrib.auth.urls")),
    path("", include("social_django.urls")),
]