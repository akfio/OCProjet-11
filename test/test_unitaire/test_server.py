import pytest
from server import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


@pytest.fixture
def club_fixture():
    data = {
        "name": "Iron Temple",
        "email": "admin@irontemple.com",
        "points": "4"
    }
    return data


@pytest.fixture
def invalid_club_fixture(club_fixture):
    club_fixture["email"] = "invalid@gmail.com"
    return club_fixture


def test_login_with_invalid_email(client, invalid_club_fixture):
    result = client.post('/showSummary', data=invalid_club_fixture)
    expected = "Sorry, that email was not found."
    assert b'Welcome to the GUDLFT Registration Portal!' in result.data
    assert expected.encode() in result.data


def test_login_with_valid_email(client, club_fixture):
    result = client.post('/showSummary', data=club_fixture)
    expected = "Welcome, " + str(club_fixture["email"])
    assert expected.encode() in result.data


def test_purchase_correct_number(client):
    data_1 = {'competition': 'Test Event', 'club': 'She Lifts', 'places': 12}
    club_1 = {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"}
    result = client.post('/purchasePlaces', data=data_1)
    total_points = int(club_1["points"]) - int(data_1["places"])
    expected = 'Points available: ' + str(total_points)
    assert expected.encode() in result.data
    assert b'Great-booking complete!' in result.data


def test_purchase_asking_more_than_12(client):
    data_2 = {'competition': 'Test Event', 'club': 'Simply Lift', 'places': 13}
    club_2 = {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"}
    result = client.post('/purchasePlaces', data=data_2)
    total_points = int(club_2["points"])
    expected = 'Points available: ' + str(total_points)
    assert expected.encode() in result.data
    assert b'PAS PLUS DE 12 PLACES PAR CLUB' in result.data


def test_purchase_club_asking_too_much(client, club_fixture):
    data_3 = {'competition': 'Test Event', 'club': 'Iron Temple', 'places': 8}
    result = client.post('/purchasePlaces', data=data_3)
    assert b'PAS ASSEZ DE POINTS DISPONIBLE' in result.data


def test_try_to_purchase_ended_competition(client, club_fixture):
    competition = 'Fall Classic'
    result = client.get('/book/'+str(competition)+'/'+str(club_fixture["name"]))
    assert b'COMPETITION OVER' in result.data


def test_try_to_purchase_valid_competition(client, club_fixture):
    competition = 'Test Event'
    result = client.get('/book/'+str(competition)+'/'+str(club_fixture["name"]))
    expected = 'Booking for ' + competition
    assert expected.encode() in result.data


def test_points_display(client, club_fixture):
    result = client.get('/points')
    expected_name = club_fixture['name']
    expected_points = str(club_fixture['points'])
    assert expected_name.encode() in result.data
    assert expected_points.encode() in result.data