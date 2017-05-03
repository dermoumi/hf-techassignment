import pytest
from django.core.urlresolvers import reverse

from mainapp.tests.fixtures import test_user
from mainapp.models import EmailJob

def test_signup_page_shows_up(client):
    response = client.get(reverse('mainapp:signup'), follow=True)
    assert response.status_code == 200

def test_signup_page_inaccessible_for_authenticated(client, test_user):
    # Have a user logged in
    client.login(username=test_user['username'], password=test_user['password'])

    # Get the client response
    response = client.get(reverse('mainapp:signup'), follow=False)

    # Make sure they're redirected to the correct page
    assert reverse('mainapp:profile') in response.get('Location')
    assert response.status_code == 302

@pytest.mark.django_db
def test_valid_user_can_sign_up(client, django_user_model):
    # Prepare signup data
    signup_data = {
        'username': 'test_sign_up_user',
        'email': 'test@signup.email',
        'password': 'p@ssword123',
        'password_confirmation': 'p@ssword123',
    }

    # Check object count in database
    old_user_count = django_user_model.objects.all().count()
    old_mail_job_count = EmailJob.objects.all().count()

    # Get the client response
    response = client.post(reverse('mainapp:signup'), signup_data)

    # Make sure that the user exists
    assert django_user_model.objects.all().count() > old_user_count
    assert django_user_model.objects.filter(username=signup_data['username'], email=signup_data['email']).exists()

    # Make sure there's a new job ongoing
    assert EmailJob.objects.all().count() > old_mail_job_count
    assert EmailJob.objects.filter(destination=signup_data['email']).exists()

def test_invalid_user_cannot_sign_up(client, django_user_model):
    # Prepare signup data
    signup_data = {
        'username': '',
        'email': 'invalid_email',
        'password': '',
        'password_confirmation': '123',
    }

    # Get the client response
    response = client.post(reverse('mainapp:signup'), signup_data)

    # Check that there are errors
    if response.context:
        for item in response.context:
            if 'form' in item:
                assert item.get('form').errors
