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


def test_login_then_purchase_places(client, club_fixture):
    result = client.post('/showSummary', data=club_fixture)
    expected = "Welcome, " + str(club_fixture["email"])
    data_1 = {'competition': 'Test Event', 'club': club_fixture["name"], 'places': 2}
    asking = client.post('/purchasePlaces', data=data_1)
    total_points = int(club_fixture["points"]) - int(data_1["places"])
    response = 'Points available: ' + str(total_points)
    assert expected.encode() in result.data
    assert b'Great-booking complete!' in asking.data
    assert response.encode() in asking.data


def test_ended_competition_then_logout(client, club_fixture):
    competition = 'Fall Classic'
    result = client.get('/book/'+str(competition)+'/'+str(club_fixture["name"]))
    assert b'COMPETITION OVER' in result.data
    logout = client.get('/logout')
    assert logout.status_code == 302


def test_purchase_then_check_points_display(client, club_fixture):
    data_1 = {'competition': 'Test Event', 'club': club_fixture['name'], 'places': 2}
    client.post('/purchasePlaces', data=data_1)
    new_points = str(int(club_fixture["points"]) - int(data_1["places"]))
    result = client.get('/points')
    assert new_points.encode() in result.data


def test_try_more_than_12_then_get_full_points(client, club_fixture):
    data = {'competition': 'Test Event', 'club': club_fixture["name"], 'places': 13}
    result = client.post('/purchasePlaces', data=data)
    assert b'PAS PLUS DE 12 PLACES PAR CLUB' in result.data
    display = client.get('/points')
    expected_points = str(club_fixture['points'])
    assert expected_points.encode() in display.data