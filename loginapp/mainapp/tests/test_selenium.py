import pytest, socket
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
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

def is_element_present(selenium, how, what):
    try:
        selenium.find_element(by=how, value=what)
    except NoSuchElementException as e:
        return False

    return True

def test_empty_login_form_shows_errors(selenium, live_server_url):
    selenium.get('%s/signup' % live_server_url)
    selenium.find_element_by_xpath("/html/body/div/div/p/a").click()
    selenium.find_element_by_xpath("//button[@type='submit']").click()
    assert is_element_present(selenium, By.XPATH, "/html/body/div/div/form/div[1]/div/div[2]/ul/li")
    assert is_element_present(selenium, By.XPATH, "/html/body/div/div/form/div[2]/div/div[2]/ul/li")
