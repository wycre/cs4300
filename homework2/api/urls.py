from django.urls import path, include

from . import views

urlpatterns = [
    path('movies', views.movies, name='movies'),
    path('movies/<pk>', views.movie, name='movie'),
    path('seats', views.seats, name='seats'),
    path('seats/<pk>', views.seats, name='book_seat'),
    path('bookings', views.bookings, name='bookings'),
]