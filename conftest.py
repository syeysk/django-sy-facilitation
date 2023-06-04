import pytest
from django.contrib.auth.models import User


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        User.objects.create_user(username='testuser', password='1234')
        User.objects.create_user(username='testuser2', password='1234')


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
