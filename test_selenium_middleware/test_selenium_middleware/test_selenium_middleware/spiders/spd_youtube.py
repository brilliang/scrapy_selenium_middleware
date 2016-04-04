# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from test_selenium_middleware.selenium_grid_server_middleware import SELENIUM_ACTIONS
from test_selenium_middleware.selenium_grid_server_middleware import WebDriverAction


class ScrollToAction(WebDriverAction):
    def act(self, driver):
        driver.execute_script("window.scrollTo(0, document.body.offsetHeight);")

    def __str__(self):
        return "scrollTo (0, document.body.offsetHeight)"


class WaitForCommentsAction(WebDriverAction):
    def act(self, driver):
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "comment-renderer-text-content"))
        )

    def __str__(self):
        return "wait for comment-renderer-text-content"


class SpdYoutubeSpider(scrapy.Spider):
    name = "spd_youtube"

    def start_requests(self):
        req_meta = {
            SELENIUM_ACTIONS: [ScrollToAction(), WaitForCommentsAction()]
        }
        yield Request(url='https://www.youtube.com/watch?v=dfTWTC7UtcQ', meta=req_meta)

    def parse(self, response):
        comm = response.xpath('//div[@class="comment-renderer-text-content"]')
        for c in comm:
            print c
