from django.shortcuts import resolve_url

USER_DATA = {'username': 'testuser', 'password': '1234'}
USER_DATA2 = {'username': 'testuser2', 'password': '1234'}


def test_creating_faci_by_unauthed_user(client):
    """Проверяет недоступность страницы создания холста незарегистрированному пользователю"""
    response = client.get(resolve_url('faci_new'))
    assert response.status_code == 401


def test_creating_faci_by_authed_user(client):
    """Проверяет доступность страницы создания холста зарегистрированному пользователю"""
    assert client.login(**USER_DATA) is True
    response = client.get(resolve_url('faci_new'))
    assert response.status_code == 200


def test_editing_aim_and_creating_faci(client):
    """Проверяет успешное редактирование цели и последующее создание нового холста"""
    assert client.login(**USER_DATA) is True
    data = {'aim': 'test aim', 'if_not_reached': 'what happend text', 'aim_type': 1}
    response = client.post(resolve_url('faci_editor_create'), data=data)
    assert response.status_code == 200
    assert response.data['success'] is True
    assert response.data['id'] == 1


def test_editing_aim(client):
    """Проверяет успешное редактирование цели у существующего холста"""
    assert client.login(**USER_DATA) is True
    data = {'aim': 'test aim', 'if_not_reached': 'what happend text', 'aim_type': 1}
    response_creating = client.post(resolve_url('faci_editor_create'), data=data)
    assert response_creating.status_code == 200
    assert response_creating.data['success'] is True

    data = {'aim': 'new test aim', 'if_not_reached': 'new what happend text', 'aim_type': 1}
    response_editing = client.post(resolve_url('faci_editor_aim', response_creating.data['id']), data=data)
    assert response_editing.status_code == 200
    assert response_editing.data['success'] is True
    assert response_editing.data['id'] == response_creating.data['id']


def test_editing_members(client):
    """Проверяет успешное редактирование цели у существующего холста"""
    assert client.login(**USER_DATA) is True
    data = {'aim': 'test aim', 'if_not_reached': 'what happend text', 'aim_type': 1}
    response_creating = client.post(resolve_url('faci_editor_create'), data=data)
    assert response_creating.status_code == 200
    assert response_creating.data['success'] is True

    data = {'aim': 'new test aim', 'if_not_reached': 'new what happend text', 'aim_type': 1}
    response_editing = client.post(resolve_url('faci_editor_aim', response_creating.data['id']), data=data)
    assert response_editing.status_code == 200
    assert response_editing.data['success'] is True
    assert response_editing.data['id'] == response_creating.data['id']

    data = {'for_what': 'for test'}
    response_member = client.post(resolve_url('faci_editor_member', response_creating.data['id'], 'testuser2'), data=data)
    assert response_member.status_code == 200
    assert response_member.data['success'] is True
