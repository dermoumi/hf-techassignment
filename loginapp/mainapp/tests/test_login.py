import pytest
from django.contrib import auth
from django.core.urlresolvers import reverse

from mainapp.tests.fixtures import test_user

def test_login_page_shows_up(client):
    response = client.get(reverse('mainapp:login'), follow=True)
    assert response.status_code == 200

def test_login_page_inaccessible_for_authenticated(client, test_user):
    # Have a user logged in
    client.login(username=test_user['username'], password=test_user['password'])

    # Get the client response
    response = client.get(reverse('mainapp:login'), follow=False)

    # Make sure they're redirected to the correct page
    assert reverse('mainapp:profile') in response.get('Location')
    assert response.status_code == 302

def test_user_can_login_successfully(client, test_user):
    # Get the client response
    response = client.post(reverse('mainapp:login'), {
        'username': test_user['username'],
        'password': test_user['password']
    }, follow=True)

    # Check if user is actually authenticated
    user = auth.get_user(client)
    assert user.is_authenticated()

    # Make sure that the form (if any?) had no errors
    if response.context:
        for item in response.context:
            if 'form' in item:
                assert not item.get('form').errors

@pytest.mark.django_db
def test_invalid_user_cannot_login(client):
    # Get the client response
    response = client.post(reverse('mainapp:login'), {
        'username': 'invalid_user',
        'password': 'invalid_password'
    })

    # Make sure that no user is authenticated
    user = auth.get_user(client)
    assert not user.is_authenticated()

    # Make sure that the form had errors
    if response.context:
        for item in response.context:
            if 'form' in item:
                assert item.get('form').errors
