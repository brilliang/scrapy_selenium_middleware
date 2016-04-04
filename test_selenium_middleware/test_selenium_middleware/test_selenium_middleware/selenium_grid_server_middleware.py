#! /usr/bin/env python
# -*- coding: UTF8 -*-

import logging

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from scrapy.http import HtmlResponse
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

SELENIUM_ACTIONS = 'selenium_actions'
_SELENIUM_DRIVER = 'selenium_driver'
_WAITING_SECONDS = 5


def check_selenium_service(command_executor):
    browser = WebDriver(command_executor=command_executor,
                desired_capabilities=DesiredCapabilities.FIREFOX)
    try:
        browser.get('https://www.youtube.com/watch?v=dfTWTC7UtcQ')
        browser.execute_script("window.scrollTo(0, document.body.offsetHeight);")
        WebDriverWait(browser, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "comment-renderer-text-content"))
            )
        assert u'comment-renderer-text-content' in browser.page_source
        logging.warning("check remote web driver (%s) successful." % command_executor)
    finally:
        browser.close()
        browser.quit()


class SeleniumGridServerMiddleware(object):

    def __init__(self, host, port):
        h = host or "127.0.0.1"
        p = port or 4444
        self.command_executor = 'http://{h}:{p}/wd/hub'.format(h=h, p=p)
        check_selenium_service(self.command_executor)

    @classmethod
    def from_crawler(cls, crawler):
        host = crawler.settings.get('SELENIUM_GRID_SERVER_HOST', None)
        port =crawler.settings.get('SELENIUM_GRID_SERVER_PORT', None)
        return cls(host, port)

    def process_request(self, request, spider):
        if hasattr(request, 'meta')  and SELENIUM_ACTIONS in request.meta:      # need selenium drive
            actions = request.meta[SELENIUM_ACTIONS]
            assert isinstance(actions, (list,tuple))
            assert all([isinstance(a, WebDriverAction) for a in actions])
            self.set_up_webdriver_in_spider(spider)
            return self._fetch_web_page(request,
                                        actions,
                                        getattr(spider, _SELENIUM_DRIVER))

    def set_up_webdriver_in_spider(self, spider):
        if not (hasattr(spider, _SELENIUM_DRIVER)
                and isinstance(getattr(spider, _SELENIUM_DRIVER), WebDriver)):
            # set the selenium driver for this spider
            driver = WebDriver(command_executor=self.command_executor,
                desired_capabilities=DesiredCapabilities.FIREFOX)
            setattr(spider, _SELENIUM_DRIVER, driver)

            def spider_closed(to_be_closed_spider):
                getattr(to_be_closed_spider, _SELENIUM_DRIVER).quit()
                logging.warning("selenium driver quit.")

            dispatcher.connect(spider_closed, signals.spider_closed)
        else:       # the spider has already been set up
            pass

    def _fetch_web_page(self, request, actions, driver):
        """
        use selenium web driver to get web page HTML of the url
        some selenium waiting action will do
        NOTE: currently only the waiting action is allowed.
        :return the whole HTML page rendered by selenium web driver
        """
        url = request.url
        try:
            logging.info('process request using selenium grid for url=%s', url)
            driver.get(url)
            for a in actions:
                a.act(driver)
                logging.debug("driver action:\t%s", str(a))
            logging.info('from selenium grid get html with length=%d for url=%s', len(driver.page_source), url)
            return HtmlResponse(url=url,
                            body = driver.page_source,
                            request=request,
                            encoding='UTF8')
        finally:
            driver.close()


class WebDriverAction(object):

    def act(self, driver):
        # do any thing with the web driver.
        raise NotImplementedError()

    def __str__(self):
        raise NotImplementedError()


if __name__ == '__main__':
    # check_selenium_service('http://127.0.0.1:4444/wd/hub')

    def test_action(my_driver):
        my_driver.execute_script("window.scrollTo(0, document.body.offsetHeight);")

    print callable(test_action)