import pytest
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

def is_element_present(selenium, how, what):
    try:
        selenium.find_element(by=how, value=what)
    except NoSuchElementException as e:
        return False

    return True

def test_empty_form(selenium, live_server):
    selenium.get('http://web:8000/signup') #< Works, needs real server up, not actual testing
    # selenium.get('%s/signup' % live_server.url.replace('localhost', 'pytest')) #< Doesn't work
    selenium.find_element_by_xpath("/html/body/div/div/p/a").click()
    selenium.find_element_by_xpath("//button[@type='submit']").click()
    assert is_element_present(selenium, By.XPATH, "/html/body/div/div/form/div[1]/div/div[2]/ul/li")
    assert is_element_present(selenium, By.XPATH, "/html/body/div/div/form/div[2]/div/div[2]/ul/li")
