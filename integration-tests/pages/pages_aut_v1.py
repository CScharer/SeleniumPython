import time
from logging import getLogger

from pages.page_base_v1 import PageBase
from pages.page_example_1 import PageExample1
from pages.page_example_2 import PageExample2

logger = getLogger(__name__)


# noinspection PyPep8Naming
class PagesAUT(PageBase):
    @property
    def Example1(self):
        return PageExample1(self.driver)

    @property
    def Example2(self):
        return PageExample2(self.driver)

    def __init__(self, driver: any, url_base: str):
        super().__init__(driver)
        self.driver = driver
        self.url_base = url_base

    @staticmethod
    def sleep(seconds):
        print(f"Sleeping for {seconds} second(s)")
        time.sleep(seconds)
