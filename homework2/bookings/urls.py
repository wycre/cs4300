from django.shortcuts import render
from django.urls import path, include
from rest_framework import routers
from .views import *



urlpatterns = [
    path('', lambda request: render(request, 'bookings/movie_list.html', {'movies': Movie.objects.all()}), name='movie_list'),
    path('pick_seat/<mpk>', list_seats, name='list_seats'),
    path('booking_history', list_bookings, name='list_bookings'),
]