from django.test import TestCase
from django.urls import reverse,resolve
from django.test import Client
import pytest


@pytest.fixture
def client():
    client = Client()
    return client


def test_connection(client):
    resp = client.get('/products/')
    assert resp.status_code == 200


def test_project_detail_view():
    path = f'/projects/{1}/'
    assert resolve(path).view_name == 'project'


def test_scraper_response(client):
    url = 'https://www.biltema.no/kontor-teknikk/batterier/akaliske-batterier/batterier-15-v-multipack-2000036570'
    response = client.post('/products/add-new-product/link/', {'url': url})
    assert response.status_code == 200
