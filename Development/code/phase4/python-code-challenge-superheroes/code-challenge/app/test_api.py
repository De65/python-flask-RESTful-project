import pytest
from flask import Flask
from app import app
from app.models import Hero, Power, HeroPower


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_heroes(client):
    response = client.get('/heroes')
    assert response.status_code == 200
    assert len(response.json) == 3

def test_get_hero_by_id(client):
    response = client.get('/heroes/1')
    assert response.status_code == 200
    assert response.json['name'] == 'Kamala Khan'



