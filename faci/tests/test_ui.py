import time

import pytest
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

PASSWORD = '1234'
WRONG_LOGIN_MESSAGE = 'Неправильный пароль или пользователь не существует'


def populate_step_one(selenium, aim=None, if_not_reached=None):
    if aim is not None:
        selenium.find_element('id', 'id_aim').send_keys(aim)

    if if_not_reached is not None:
        selenium.find_element('id', 'id_if_not_reached').send_keys(if_not_reached)

    selenium.find_element('id', 'btn_save_aim').send_keys(Keys.ENTER)
    time.sleep(2)


def add_member(invited=None, for_what=None):
    pass


def login(selenium, username, password):
    btn_open_login_form = selenium.find_element('id', 'btn_toggle_login_box')
    field_username = selenium.find_element('id', 'id_for_label_username')
    field_password = selenium.find_element('id', 'id_for_label_password')
    btn_send_login_form = selenium.find_element('id', 'login_button')

    btn_open_login_form.send_keys(Keys.ENTER)
    field_username.send_keys(username)
    field_password.send_keys(password)

    btn_send_login_form.send_keys(Keys.ENTER)
    time.sleep(2)


def registrate(selenium, username, password, password_repeat, email):
    btn_open_registration_form = selenium.find_element('id', 'btn_toggle_registration_box')
    field_username = selenium.find_element(By.CSS_SELECTOR, '#registration_box #id_for_label_username')  # TODO: Переименовать поле, чтобы не дублировалось
    field_password = selenium.find_element('id', 'id_for_label_password1')
    field_password_repeat = selenium.find_element('id', 'id_for_label_password2')
    field_email = selenium.find_element('id', 'id_for_label_email')
    btn_send_registrate_form = selenium.find_element('id', 'registrate_button')

    btn_open_registration_form.send_keys(Keys.ENTER)
    field_username.send_keys(username)
    field_password.send_keys(password)
    field_password_repeat.send_keys(password_repeat)
    field_email.send_keys(email)

    btn_send_registrate_form.send_keys(Keys.ENTER)
    time.sleep(2)


def test_registration(live_server, faker):
    selenium = webdriver.Chrome()
    selenium.get(live_server.url)

    username = faker.user_name()
    password = faker.password()
    email = faker.email()
    assert User.objects.filter(username=username).first() is None
    registrate(selenium, username, password, password, email)

    assert User.objects.filter(username=username).first() is not None
    assert selenium.find_element('id', 'logout_button')


def test_ui_login(live_server, user):
    selenium = webdriver.Chrome()
    selenium.get(live_server.url)

    login(selenium, user.username, user.password)
    with pytest.raises(NoSuchElementException):
        selenium.find_element('id', 'login_bad_message')

    assert selenium.find_element('id', 'logout_button')


def test_ui_login_wrong_username(live_server):
    selenium = webdriver.Chrome()
    selenium.get(live_server.url)
    login(selenium, 'unexisted user', PASSWORD)
    assert WRONG_LOGIN_MESSAGE in selenium.find_element('id', 'login_bad_message').text


def test_ui_login_absent_username(live_server):
    selenium = webdriver.Chrome()
    selenium.get(live_server.url)
    login(selenium, '', PASSWORD)
    assert WRONG_LOGIN_MESSAGE in selenium.find_element('id', 'login_bad_message').text


def test_ui(live_server, user):
    selenium = webdriver.Chrome()

    # Go to main page and login

    selenium.get(live_server.url)
    login(selenium, user.username, user.password)

    # Go to faci list page

    selenium.get(live_server + '/faci/')
    time.sleep(2)

    # Go to add faci page

    selenium.find_element('id', 'add_token_button').send_keys(Keys.ENTER)  # TODO: Удалить ID add_token_button  в шаблоне
    time.sleep(2)

    form_sheet_members = selenium.find_element(By.CSS_SELECTOR, '#members_form .form_sheet')
    assert 'd-none' not in form_sheet_members.get_attribute('class')

    # Populate step 1

    populate_step_one(
        selenium,
        aim='Создать новую версию устройства',
        if_not_reached='Упадут продажи, т.к. Текущая вресия моральна устарела',
    )

    assert 'd-none' in form_sheet_members.get_attribute('class')

    # Add member

    add_member(invited='strong_puma', for_what='Дизайн')


# TODO: добавить тесты для авторизации с пустым паролем, для авторизации с неактивным пользователем
