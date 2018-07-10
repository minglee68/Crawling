import scrapy
from scrapy.utils.response import open_in_browser

import lxml.etree
import lxml.html


BASE_URL = "https://hisnet.handong.edu"
PAGES = ['/main.php']

class LoginSpider(scrapy.Spider):
    name = 'login'
    start_urls = ['https://hisnet.handong.edu/login/login.php']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            formnumber=2,
            formdata={'part':'', 'f_name':'', 'agree':'', 'Language':'Korean', 'id': 'minglee68', 'password': 'aa', 'x':'10', 'y':'47'},
            clickdata={'src':'/2012_images/intro/btn_login.gif'},
            callback=self.goto_mainpage
        )

    def goto_mainpage(self, response):
        print(response)
        for page in PAGES:
            yield scrapy.http.Request(
                url=BASE_URL + page,
                callback=self.after_login
            )

    def after_login(self, response):
        print("hello!")
        SET_SELECTOR = 'body'
        for someset in response.css(SET_SELECTOR):
            IMAGE_SELECTOR = 'div ::attr(id)'
            yield {
                'img' : someset.css(IMAGE_SELECTOR).extract_first()
            }

