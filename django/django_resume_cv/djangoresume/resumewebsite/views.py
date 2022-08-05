from django.shortcuts import render

def home(request):
    return render(request, 'home.html', {}) #passing empty variable

# Create your views here.
