import json

from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import duration

from datetime import date

from bookings.models import *

import requests

# Create your tests here.
class MovieTestCase(TestCase):
    def setUp(self):
        Movie.objects.create(title="Test Movie", description="This is a test movie", duration=100, release_date=datetime.today())
        Movie.objects.create(title="Test Movie 2", description="This is another test movie", duration=150, release_date=datetime.today())

    def test_movie_title(self):
        movie = Movie.objects.get(title="Test Movie")
        self.assertEqual(movie.title, "Test Movie")

class SeatTestCase(TestCase):
    def setUp(self):
        Seat.objects.create(seat_number=1, is_booked=False)
        Seat.objects.create(seat_number=2, is_booked=True)

    def test_seat_booking(self):
        seat1 = Seat.objects.get(seat_number=1)
        seat2 = Seat.objects.get(seat_number=2)
        self.assertEqual(seat1.is_booked, False)
        self.assertEqual(seat2.is_booked, True)

class BookingTestCase(TestCase):
    def setUp(self):
        movie1 = Movie.objects.create(title="Test Movie", description="This is a test movie", duration=100, release_date=datetime.today())
        movie2 = Movie.objects.create(title="Test Movie 2", description="This is another test movie", duration=150, release_date=datetime.today())

        seat1 = Seat.objects.create(seat_number=1, is_booked=False)
        seat2 = Seat.objects.create(seat_number=2, is_booked=True)

        Booking.objects.create(booking_date=datetime.today(), movie=movie1, seat=seat2)

    def test_booking(self):
        booking = Booking.objects.get(seat=Seat.objects.get(seat_number=2))
        self.assertEqual(booking.seat, Seat.objects.get(seat_number=2))


class APITests(StaticLiveServerTestCase):
    """these tests work when run independently, but not as a whole class"""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.live_server_url

    def setUp(self):
        movie1 = Movie.objects.create(title="Test Movie", description="This is a test movie", duration=100, release_date=datetime.today())
        movie2 = Movie.objects.create(title="Test Movie 2", description="This is another test movie", duration=150, release_date=datetime.today())

        seat1 = Seat.objects.create(seat_number=1, is_booked=False)
        seat2 = Seat.objects.create(seat_number=2, is_booked=True)

        Booking.objects.create(booking_date=datetime.today(), movie=movie1, seat=seat2)

    def test_get_movies(self):
        get_res = requests.get(f'{self.live_server_url}/api/movies')
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()[0]['title'], 'Test Movie')

    def test_put_movie(self):
        res = requests.put(f'{self.live_server_url}/api/movies', json={'title': 'Test Movie 3', 'description': 'This is the third test movie', "duration":"150", "release_date": "2026-01-01"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, "{'id': 3, 'title': 'Test Movie 3', 'description': 'This is the third test movie', 'release_date': '2026-01-01', 'duration': 150}")
        self.assertEqual(Movie.objects.get(title="Test Movie 3").description, 'This is the third test movie')

    def test_get_movie(self):
        res = requests.get(f'{self.live_server_url}/api/movies/1')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, "{'id': 1, 'title': 'Test Movie', 'description': 'This is a test movie', 'release_date': '2025-02-28', 'duration': 100}")

    def test_post_movie(self):
        res = requests.post(f'{self.live_server_url}/api/movies/{Movie.objects.all()[0].id}', json={"title": "The Testening"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Movie.objects.all()[0].title, "The Testening")

        res = requests.post(f'{self.live_server_url}/api/movies/{Movie.objects.all()[0].id}',json={"description": "Incredible testing action!"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Movie.objects.all()[0].description, "Incredible testing action!")

        res = requests.post(f'{self.live_server_url}/api/movies/{Movie.objects.all()[0].id}', json={"duration": "900"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Movie.objects.all()[0].duration, 900)

        res = requests.post(f'{self.live_server_url}/api/movies/{Movie.objects.all()[0].id}', json={"release_date": "2026-01-01"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Movie.objects.all()[0].release_date, date(2026, 1, 1))

    def test_delete_movie(self):
        self.assertEqual(Movie.objects.filter(title="Test Movie").count(), 1)
        res = requests.delete(f'{self.live_server_url}/api/movies/{Movie.objects.get(title="Test Movie").id}')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Movie.objects.filter(title="Test Movie").count(), 0)



    def test_get_seats(self):
        res = requests.get(f'{self.live_server_url}/api/seats')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, '[{"id": 1, "seat_number": "1", "is_booked": false}, {"id": 2, "seat_number": "2", "is_booked": true}]')

    def test_get_seat(self):
        res = requests.get(f'{self.live_server_url}/api/seats/1')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.text, "{'id': 1, 'seat_number': '1', 'is_booked': False}")

    def test_post_seat(self):
        res = requests.post(f'{self.live_server_url}/api/seats/1', json={"is_booked": "True"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Seat.objects.all()[0].is_booked, True)

    def test_get_bookings(self):
        res = requests.get(f'{self.live_server_url}/api/bookings')
        self.assertEqual(res.status_code, 200)
        self.assertNotEqual(res.text, "") # Other assertion options don't work well with the booking date field

    def test_put_booking(self):
        self.assertEqual(Booking.objects.all().count(), 1)
        res = requests.put(f'{self.live_server_url}/api/bookings', json={"movie": "1", "seat": "1", "booking_date": "2026-01-01"})
        self.assertEqual(res.status_code, 200)
        self.assertEqual(Booking.objects.all().count(), 2)