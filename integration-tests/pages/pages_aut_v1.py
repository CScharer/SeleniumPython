import time
from logging import getLogger

from pages.page_base_v1 import PageBase
from pages.page_example_1 import PageExample1
from pages.page_example_2 import PageExample2

logger = getLogger(__name__)


class PagesAUT(PageBase):
    @property
    def Example1(self):
        return PageExample1(self.__driver)

    @property
    def Example2(self):
        return PageExample2(self.__driver)

    def __init__(self, driver: any, url_base: str):
        super().__init__(driver)
        self.__driver = driver
        self.__base_url = url_base

    @staticmethod
    def sleep(seconds):
        print(f"Sleeping for {seconds} second(s)")
        time.sleep(seconds)
