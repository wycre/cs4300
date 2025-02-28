from django.shortcuts import render

from .models import *

# Create your views here.
def index(request):
    context = {}
    context["movies"] = Movie.objects.all()

    context["nav_movie_list"] = True
    return render(request, "bookings/movie_list.html", context)