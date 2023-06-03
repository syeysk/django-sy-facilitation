import pytest
from django.contrib.auth.forms import UserCreationForm


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        user_creation_form = UserCreationForm({'username': 'testuser', 'password1': '1234', 'password2': '1234'})
        if user_creation_form.is_valid():
            user_creation_form.save()
        else:
            raise ValueError('creating user is fail')


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass
