This is a simplest [Scrapy](https://github.com/scrapy/scrapy) project. current at its 1.05 version.

Inside there is a download middleware working with a [selenium grid](http://www.seleniumhq.org/docs/), which is a web browser programming interface and is very suitable for javascript rendering job for web data grabbing.

In a scrapy [Spider ](http://doc.scrapy.org/en/latest/topics/spiders.html), you only need set up a flag of SELENIUM, and optional some action inside the browser, such as click a button, or waiting for some elements inside the webpage. Spiders without the SELENIUM flag, will go the original way.

Also, the selenium grid setting is easy, just follow this [instruction](http://www.seleniumhq.org/docs/07_selenium_grid.jsp).
