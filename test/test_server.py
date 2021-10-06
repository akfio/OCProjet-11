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


def test_points_display(client, club_fixture):
    result = client.get('/points')
    expected_name = club_fixture['name']
    expected_points = str(club_fixture['points'])
    assert expected_name.encode() in result.data
    assert expected_points.encode() in result.data


def test_points_display_after_purchase(client, club_fixture):
    data_1 = {'competition': 'Test Event', 'club': club_fixture['name'], 'places': 2}
    client.post('/purchasePlaces', data=data_1)
    new_points = str(int(club_fixture["points"]) - int(data_1["places"]))
    result = client.get('/points')
    assert new_points.encode() in result.data