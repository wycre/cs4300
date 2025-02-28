import json

from django.forms import Form
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import *


# I will NOT be using ViewSets unless a good argument is made in favor of using them

# Create your views here.
def index(request):
    context = {}
    context["movies"] = Movie.objects.all()
    return render(request, "bookings/movie_list.html", context)

def list_seats(request, mpk):
    if request.method == "GET":
        context = {}
        context["seats"] = Seat.objects.all()
        context["movie"] = Movie.objects.get(pk=mpk)
        return render(request, "bookings/seat_booking.html", context)
    elif request.method == "POST":
        print(request.POST)
        context = {}

        try:
            seat_id = request.POST.get("seat", False)
            seat = Seat.objects.get(id=seat_id)

            movie = Movie.objects.get(id=mpk)

            context["seat"] = seat

            seat.is_booked = True
            seat.save()

            booking = Booking.objects.create(seat=seat, movie=movie)
            booking.save()
            return redirect('list_bookings')
        except Movie.DoesNotExist:
            return HttpResponse(status=404, content="Movie does not exist")
        except Seat.DoesNotExist:
            return HttpResponse(status=404, content="Seat does not exist")

def list_bookings(request,):
    if request.method == "GET":
        bookings = Booking.objects.all()
        context = {"bookings": bookings}
        return render(request, 'bookings/booking_history.html', context)
