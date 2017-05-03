import pytest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from mainapp.tests.fixtures import selenium, live_server_url

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
