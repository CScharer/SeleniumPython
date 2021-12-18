import logging
import sys
import time
from datetime import datetime, timedelta

import pytest
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger(__name__)


class PageBase:
    BODY_PAGE = (By.TAG_NAME, "body")
    HTML_PAGE = (By.TAG_NAME, "html")
    SPINNER = (By.CLASS_NAME, "spinner")

    default_soft_timeout = 15
    default_hard_timeout = 60

    def __init__(self, driver, default_wait_time=10):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, timeout=default_wait_time)

    @staticmethod
    def clear_input(element):
        key = Keys.COMMAND if sys.platform == "darwin" else Keys.CONTROL
        element.send_keys(key + "a")
        element.send_keys(Keys.DELETE)
        element.clear()

    def click_on_coordinate(self, width, height):
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(self.driver.find_element(*self.BODY_PAGE), 1, 1)
        action.move_by_offset(width, height)
        action.click()
        action.perform()

    def click_position_on_map(self, position):
        action = ActionChains(self.driver)
        browser_sizes = self.driver.get_window_size()
        width = browser_sizes["width"]
        height = browser_sizes["height"]
        action.move_to_element_with_offset(self.driver.find_element(*self.BODY_PAGE), 1, 1)
        if position == "left":
            action.move_by_offset(width / 2 - 500, height / 2)
        elif position == "right":
            action.move_by_offset(width / 2 + 500, height / 2)
        elif position == "up":
            action.move_by_offset(width / 2, height / 2 - 200)
        elif position == "down":
            action.move_by_offset(width / 2, height / 2 + 200)
        else:
            action.move_by_offset(width / 2, height / 2)
        action.click()
        action.perform()

    def is_text_present(self, text):
        page_text = self.wait_for_and_get_element(self.BODY_PAGE).text
        return text in page_text

    def scroll_to_bottom(self):
        self.driver.find_element(*self.HTML_PAGE).send_keys(Keys.PAGE_DOWN)

    def switch_tab(self, window_name):
        self.driver.switch_to.window(window_name)

    # Use this method to parameterized a locator
    # Example: YOUR_LOCATOR_NAME = (By.XPATH,'//*[@data-qa="your locator"]//*[text()="{}"]')
    # Usage:  def your_method(self, text):
    #         return self.verify_element_text(self.YOUR_LOCATOR_NAME, text)
    def verify_element_text(self, locator, text):
        locator_type, locator = locator
        return self.driver.find_element(locator_type, locator.format(text))

    def wait_for_and_get_element(self, element, hard_timeout=default_hard_timeout, soft_timeout=default_soft_timeout):

        start_time = datetime.now()
        hard_finish_time = start_time + timedelta(seconds=hard_timeout)
        soft_finish_time = start_time + timedelta(seconds=soft_timeout)
        found_element = None
        self.driver.implicitly_wait(1)

        while datetime.now() < hard_finish_time:
            time.sleep(1)
            try:
                found_element = self.wait.until(EC.visibility_of_element_located(element))
                assert type(found_element) is WebElement
                break

            except Exception as exception_net:
                logger.debug(str(exception_net))
                pass

        self.driver.implicitly_wait(30)

        if type(found_element) is not WebElement:
            pytest.fail(f"--- Hard timeout after {hard_timeout} seconds --- Element: {element}")

        if datetime.now() > soft_finish_time:
            logger.warning(f"Soft timeout after {soft_timeout} seconds --- Element: {element}")

        return found_element

    def wait_for_and_get_element_is_clickable(
        self, element, hard_timeout=default_hard_timeout, soft_timeout=default_soft_timeout
    ):
        start_time = datetime.now()
        hard_finish_time = start_time + timedelta(seconds=hard_timeout)
        soft_finish_time = start_time + timedelta(seconds=soft_timeout)
        found_element = None
        self.driver.implicitly_wait(1)

        while datetime.now() < hard_finish_time:
            time.sleep(1)
            try:
                found_element = self.wait.until(EC.element_to_be_clickable(element))
                assert type(found_element) is WebElement
                break

            except Exception as exception_net:
                logger.debug(str(exception_net))
                pass

        self.driver.implicitly_wait(30)

        if type(found_element) is not WebElement:
            pytest.fail(f"--- Hard timeout after {hard_timeout} seconds --- Element: {element}")

        if datetime.now() > soft_finish_time:
            logger.warning(f"Soft timeout after {soft_timeout} seconds --- Element: {element}")

        return found_element

    def wait_for_element_to_disappear(
        self, element, hard_timeout=default_hard_timeout, soft_timeout=default_soft_timeout
    ):

        start_time = datetime.now()
        hard_finish_time = start_time + timedelta(seconds=hard_timeout)
        soft_finish_time = start_time + timedelta(seconds=soft_timeout)
        invisible_element = None
        self.driver.implicitly_wait(1)

        while datetime.now() < hard_finish_time:
            time.sleep(1)
            try:
                invisible_element = self.wait.until(EC.invisibility_of_element_located(element))
                assert invisible_element
                break

            except Exception as exception_net:
                logger.debug(str(exception_net))
                continue

        self.driver.implicitly_wait(30)

        if not invisible_element:
            pytest.fail(f"--- Hard timeout after {hard_timeout} seconds --- Element: {element}")

        if datetime.now() > soft_finish_time:
            logger.warning(f"Soft timeout after {soft_timeout} seconds --- Element: {element}")

        return invisible_element

    def wait_for_spinner_disappear(self):
        self.wait_for_element_to_disappear(self.SPINNER)
