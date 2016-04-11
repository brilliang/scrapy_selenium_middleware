# -*- coding: utf-8 -*-

BOT_NAME = 'test_selenium_middleware'

SPIDER_MODULES = ['test_selenium_middleware.spiders']
NEWSPIDER_MODULE = 'test_selenium_middleware.spiders'

DOWNLOADER_MIDDLEWARES = {
    'test_selenium_middleware.selenium_grid_server_middleware.SeleniumGridServerMiddleware': 0,
}

DOWNLOAD_DELAY=2

SELENIUM_GRID_SERVER_HOST = "127.0.0.1"
SELENIUM_GRID_SERVER_PORT = 4444
