from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class LoginTests(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(LoginTests, cls).setUpClass()
        cls.selenium = webdriver.Remote(
           command_executor='http://selenium-chrome:4444/wd/hub',
           desired_capabilities=DesiredCapabilities.CHROME)
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(LoginTests, cls).tearDownClass()

    def test_empty_form(self):
        driver = self.selenium
        driver.get('%s/signup' % self.live_server_url)
        driver.find_element_by_link_text(u"Log in »").click()
        driver.find_element_by_xpath("//button[@type='submit']").click()
        self.assertTrue(self.is_element_present(By.XPATH, "/html/body/div/div/form/div[1]/div/div[2]/ul/li"))
        self.assertTrue(self.is_element_present(By.XPATH, "/html/body/div/div/form/div[2]/div/div[2]/ul/li"))

    def is_element_present(self, how, what):
        try: self.selenium.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
