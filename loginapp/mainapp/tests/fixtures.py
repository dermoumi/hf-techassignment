import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

@pytest.fixture(scope="module")
def selenium():
    driver = webdriver.Remote(
        command_executor='http://selenium-chrome:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME)
    driver.implicitly_wait(2)
    yield driver
    driver.quit()

@pytest.fixture(scope="module")
def live_server_url():
    return 'http://web:8000'

@pytest.fixture()
def test_user(db, django_user_model):
    user_data = {
        'username': 'test_user',
        'email': 'test@email.address',
        'password': 'p@ssword123',
        'instance': None
    }

    test_user = django_user_model(username=user_data.get('username'), email=user_data.get('email'))
    test_user.set_password(user_data.get('password'))
    test_user.save()
    user_data['instance'] = test_user

    yield user_data
    test_user.delete()

