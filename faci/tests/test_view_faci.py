import pytest
from django.contrib.auth.models import User
from django.shortcuts import resolve_url

# DJANGO_SETTINGS_MODULE


def test_create_faci_by_unauthed_user(client):
    response = client.get(resolve_url('faci_new'))
    assert response.status_code == 401


def test_create_faci_by_authed_user(client):
    res = client.login(username='testuser', password='1234')
    assert res is True
    response = client.get(resolve_url('faci_new'))
    assert response.status_code == 200
