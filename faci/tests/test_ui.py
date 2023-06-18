from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

USERNAME = 'clever_cat'
PASSWORD = '1234-clever_cat'


def test_ui():
    selenium = webdriver.Chrome()
    selenium.get('http://127.0.0.1:8002/')

    # Login

    btn_open_login_form = selenium.find_element('id', 'btn_toggle_login_box')
    field_username = selenium.find_element('id', 'id_for_label_username')
    field_password = selenium.find_element('id', 'id_for_label_password')
    btn_send_login_form = selenium.find_element('id', 'login_button')

    btn_open_login_form.send_keys(Keys.ENTER)
    field_username.send_keys(USERNAME)
    field_password.send_keys(PASSWORD)
    btn_send_login_form.send_keys(Keys.ENTER)

    selenium.get('http://127.0.0.1:8002/faci/')

    # Populate step 1

    selenium.find_element('id', 'add_token_button').send_keys(Keys.ENTER)
    selenium.find_element('id', 'id_aim').send_keys('Создать новую версию устройства')
    selenium.find_element('id', 'id_if_not_reached').send_keys('Упадут продажу, т.к. Текущая вресия моральна устарела')
    selenium.find_element('id', 'btn_save_aim').send_keys(Keys.ENTER)

    #form_sheet



    assert 1 == 1
