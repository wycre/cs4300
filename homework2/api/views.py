import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from bookings.models import *

from .util import *

# Create your views here.
@csrf_exempt
def movies(request):
    response = HttpResponse(content_type='application/json')

    # Get info on all movies
    if request.method == 'GET':
        all_movies = Movie.objects.all()
        all_movies_list = []
        for movie in all_movies:
            all_movies_list.append(MovieSerializer(movie).data)

        response.status_code = 200
        response.write(json.dumps(all_movies_list))

    # make a new movie
    elif request.method == 'PUT':
        data = json.loads(request.body)
        name = data['title']
        description = data['description']
        duration = data['duration']
        release_date = data['release_date']

        movie = MovieSerializer().create(data)

        response.status_code = 200
        response.write(str(MovieSerializer(movie).data))


    return response

@csrf_exempt
def movie(request, pk):
    response = HttpResponse(content_type='application/json')

    # Get info on one movie
    if request.method == 'GET':
        mov = Movie.objects.get(pk=pk)
        data = MovieSerializer(mov).data

        response.status_code = 200
        response.write(data)

    # Update a movie
    elif request.method == 'POST':
        mov = Movie.objects.get(pk=pk)

        data = json.loads(request.body)
        title = data.get('title', False)
        description = data.get('description', False)
        duration = data.get('duration', False)
        release_date = data.get('release_date', False)

        if title:
            mov.title = title
        if description:
            mov.description = description
        if duration:
            mov.duration = duration
        if release_date:
            mov.release_date = release_date

        mov.save()

        response.status_code = 200
        response.write('{"result":"ok","data":'+str(MovieSerializer(mov).data)+'}')

    # Delete a movie
    elif request.method == 'DELETE':
        mov = Movie.objects.get(pk=pk)
        mov.delete()

        response.status_code = 200
        response.write('{"result":"ok"}')

    return response

@csrf_exempt
def seats(request, pk=False):
    response = HttpResponse(content_type='application/json')
    # Get all seats or details on one seat
    if request.method == 'GET':
        if pk:
            seat = Seat.objects.get(pk=pk)
            data = SeatSerializer(seat).data

            response.status_code = 200
            response.write(data)
        else:
            seats = Seat.objects.all()

            seats_list = []
            for seat in seats:
                seats_list.append(SeatSerializer(seat).data)

            response.status_code = 200
            response.write(json.dumps(seats_list))

    # Book a seat
    elif request.method == 'POST':
        if not pk:
            response.status_code = 405
            response.write('{"status": 405, "message": "POST not allowed if no seat ID is defined"}')
        else:
            seat = Seat.objects.get(pk=pk)
            data = json.loads(request.body)

            book_status = data.get('is_booked', None)
            if book_status is not None:
                book_status = data.get('is_booked')
                if book_status:
                    seat.is_booked = True
                else:
                    seat.is_booked = False
                seat.save()
                response.status_code = 200
                response.write('{"result":"ok"}')
            else:
                response.status_code = 400
                response.write('{"status": 400, "message": "is_booked value is required"}')

    return response

@csrf_exempt
def bookings(request):
    response = HttpResponse(content_type='application/json')
    # get full booking history
    if request.method == 'GET':
        all_bookings = Booking.objects.all()
        all_bookings_list = []
        for booking in all_bookings:
            all_bookings_list.append(BookingSerializer(booking).data)

        response.status_code = 200
        response.write(json.dumps(all_bookings_list))

    # Make new booking
    elif request.method == 'PUT':
        data = json.loads(request.body)

        mov = Movie.objects.get(pk=data.get('movie', False))
        seat = Seat.objects.get(pk=data.get('seat', False))
        booking_date = data.get('booking_date', False)

        if not mov or not seat or not booking_date:
            response.status_code = 400
            response.write('{"status": 400, "message": "movie, seat, and booking_date are required"}')

        booking = Booking.objects.create(movie=mov, seat=seat, booking_date=booking_date)
        booking.save()

        response.status_code = 200
        response.write('{"status": "ok"}')

    return response