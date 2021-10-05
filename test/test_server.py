import unittest
from unittest.mock import patch
import requests
from flask import request, jsonify

import pytest

import server
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

@pytest.fixture
def competition():
    competition = "Test Event"
    return competition

@pytest.fixture
def club():
    club = "She Lifts"
    return club


def test_try_to_purchase_ended_competition(client, competition, club):
    result = client.get('/book/<competition>/<club>', query_string={'competition': competition, 'club': club})
    assert b'COMPETITION OVER' in result.data

"""



def test_purchase_asking_more_than_12(client):
    data_2 = {'competition': 'Test Event', 'club': 'Simply Lift', 'places': 13}
    club_2 = {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}
    result = client.post('/purchasePlaces', data=data_2)
    total_points = int(club_2["points"])
    expected = 'Points available: ' + str(total_points)
    assert expected.encode() in result.data
    assert b'PAS PLUS DE 12 PLACES PAR CLUB' in result.data


def test_purchase_club_asking_too_much(client):
    data_3 = {'competition': 'Test Event', 'club': 'Iron Temple', 'places': 8}
    club_3 = {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"}
    result = client.post('/purchasePlaces', data=data_3)
    total_points = int(club_3["points"])
    expected = 'Points available: ' + str(total_points)
    assert expected.encode() in result.data
    assert b'PAS ASSEZ DE POINTS DISPONIBLE' in result.data

class Test_purchase(unittest.TestCase):
    url = 'http://127.0.0.1:5000/purchasePlaces'

    def test_purchase_correct_number(self):
        r = requests.post(self.url, self.data_1)
        total = int(self.club_1["points"]) - int(self.data_1["places"])
        assert 'Points available: ' + str(total) in r.text
        assert 'Great-booking complete!' in r.text

    def test_purchase_asking_more_than_12(self):
        r = requests.post(self.url, self.data_2)
        total = int(self.club_2["points"])
        assert 'Points available: ' + str(total) in r.text
        assert 'PAS PLUS DE 12 PLACES PAR CLUB' in r.text

    def test_purchase_club_asking_too_much(self):
        r = requests.post(self.url, self.data_3)
        total = int(self.club_3["points"])
        assert 'Points available: ' + str(total) in r.text
        assert 'PAS ASSEZ DE POINTS DISPONIBLE' in r.text


class Test_purchase(unittest.TestCase):
    def setUp(self):
        mock_clubs = patch('server.loadClubs').start()
        mock_competitions = patch('server.loadCompetitions').start()
        self.addCleanup(patch.stopall)
        
def test_pur():
    app = server.app
    client = app.test_client()
    url = '/purchasePlaces'
    response = client.get(url)
    assert response.status_code == 200

def test_purchase_2(purchase_fixture):
    app = server.app
    client = app.test_client()
    resp = client.post('/purchasePlaces', data=purchase_fixture)
    reponse = resp.data.decode('utf8').replace("'", '"')
    assert 'Book Places' in reponse


@pytest.fixture
def club_fixture():
    data = {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    }
    return data


@pytest.fixture
def compet_fixture():
    data = {
        "name": "Test Event",
        "date": "2022-10-22 13:30:00",
        "numberOfPlaces": "246"
    }
    return data

@pytest.fixture
def purchase_fixture():
    data = {
        'competition': 'Test Event',
        'club': 'Iron Temple',
        'places': 4
    }
    return data


def test_show_summary(club_fixture):
    url = 'http://127.0.0.1:5000/showSummary'
    info = club_fixture
    r = requests.post(url, info)
    assert r.status_code == 200



class Test_purchase(unittest.TestCase):
    url = 'http://127.0.0.1:5000/purchasePlaces'

    data_3 = {
        'competition': 'Test Event',
        'club': 'Iron Temple',
        'places': 8
    }

    data_2 = {
        'competition': 'Test Event',
        'club': 'Simply Lift',
        'places': 13
    }

    data_1 = {
        'competition': 'Test Event',
        'club': 'She Lifts',
        'places': 1
    }

    club_3 = {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    }

    club_2 = {
        "name": "Simply Lift",
        "email": "john@simplylift.co",
        "points": "13"
    }

    club_1 = {
        "name": "She Lifts",
        "email": "kate@shelifts.co.uk",
        "points": "12"
    }

    def test_purchase_correct_number(self):
        r = requests.post(self.url, self.data_1)
        total = int(self.club_1["points"]) - int(self.data_1["places"])
        assert 'Points available: ' + str(total) in r.text
        assert 'Great-booking complete!' in r.text

    def test_purchase_asking_more_than_12(self):
        r = requests.post(self.url, self.data_2)
        total = int(self.club_2["points"])
        assert 'Points available: ' + str(total) in r.text
        assert 'PAS PLUS DE 12 PLACES PAR CLUB' in r.text

    def test_purchase_club_asking_too_much(self):
        r = requests.post(self.url, self.data_3)
        total = int(self.club_3["points"])
        assert 'Points available: ' + str(total) in r.text
        assert 'PAS ASSEZ DE POINTS DISPONIBLE' in r.text
"""