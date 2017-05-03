import pytest
from django.core.urlresolvers import reverse

from mainapp.tests.fixtures import test_user

def test_profile_page_inaccessible_to_anonymous(client):
    response = client.get(reverse('mainapp:profile'))

    assert response.status_code == 302
    assert reverse('mainapp:login') in response.get('Location')

def test_profile_page_accessible_to_authenticatde(client, test_user):
    # Login a user
    client.login(username=test_user['username'], password=test_user['password'])

    # Get client response
    response = client.get(reverse('mainapp:profile'), follow=False)

    assert response.status_code == 200