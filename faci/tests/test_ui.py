import time

import pytest
from django.test import LiveServerTestCase
from selenium import webdriver

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

USERNAME = 'clever_cat'
PASSWORD = '1234-clever_cat'
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


def test_ui_login():
    selenium = webdriver.Chrome()

    selenium.get('http://127.0.0.1:8002/')

    login(selenium, USERNAME, PASSWORD)
    with pytest.raises(NoSuchElementException):
        selenium.find_element('id', 'login_bad_message')

    assert selenium.find_element('id', 'logout_button')


def test_ui_login_wrong_username():
    selenium = webdriver.Chrome()
    selenium.get('http://127.0.0.1:8002/')
    login(selenium, 'unexisted user', PASSWORD)
    assert WRONG_LOGIN_MESSAGE in selenium.find_element('id', 'login_bad_message').text


def test_ui_login_absent_username():
    selenium = webdriver.Chrome()
    selenium.get('http://127.0.0.1:8002/')
    login(selenium, '', PASSWORD)
    assert WRONG_LOGIN_MESSAGE in selenium.find_element('id', 'login_bad_message').text


def test_ui():
    selenium = webdriver.Chrome()

    # Go to main page and login

    selenium.get('http://127.0.0.1:8002/')
    login(selenium, USERNAME, PASSWORD)

    # Go to faci list page

    selenium.get('http://127.0.0.1:8002/faci/')
    time.sleep(2)

    # Go to add faci page

    selenium.find_element('id', 'add_token_button').send_keys(Keys.ENTER)
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
