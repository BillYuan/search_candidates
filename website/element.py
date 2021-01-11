import logging
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

logger = logging.getLogger(u"sr")
DEBUG_DELAY = 2


class Element(object):

    def __init__(self, browser, locator):
        self.browser = browser
        self.timeout = 30
        self.locator = locator

    def input_value(self, value):
        browser = self.browser
        WebDriverWait(browser, self.timeout).until(
            lambda browser: browser.find_element(*self.locator))
        ActionChains(browser).move_to_element(browser.find_element(*self.locator)).perform()
        ActionChains(browser).click().perform()
        browser.find_element(*self.locator).clear()
        browser.find_element(*self.locator).send_keys(value)

    def click(self):
        element = self.element
        if element:
            element.click()
            if logging.DEBUG == logger.level:
                time.sleep(DEBUG_DELAY)

    @property
    def element(self):
        browser = self.browser
        WebDriverWait(browser, self.timeout).until(
            lambda browser: browser.find_element(*self.locator))
        element = browser.find_element(*self.locator)
        return element

    @property
    def elements(self):
        browser = self.browser
        WebDriverWait(browser, self.timeout).until(
            lambda browser: browser.find_elements(*self.locator))
        elements = browser.find_elements(*self.locator)
        return elements
