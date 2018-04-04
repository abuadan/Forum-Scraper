# -*- coding: utf-8 -*-
from forum_scraper.items import PostItem, BoardItem, ProfileItem
from scrapy.linkextractors import LinkExtractor
from scrapy.exceptions import IgnoreRequest
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Request
from scrapy.spiders import Rule
from bs4 import BeautifulSoup
from datetime import datetime
import time


class BitcointalkSpider(CrawlSpider):
    name = 'bitcointalk'
    allowed_domains = ['bitcointalk.org']
    start_urls = ['http://bitcointalk.org/']

    rules = [
        Rule(
                LinkExtractor(
                        allow=('/index.php\?board=[0-9][.][0-9]',
                               '/index.php\?topic=[0-9][.][0-9]',),
                        deny=('/index.php?action=register',
                              '/index.php?action=login',
                              '/index.php?action=search;advanced',
                              '/index.php?action=help',),
                        canonicalize=True,
                        unique=True
                ),
                follow=True,
                callback='parse_item',
        )
    ]

    # Method which starts the requests by visiting all URLs specified in start_urls
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse, dont_filter=False)

    def parse_board(self, response):
        board_item = BoardItem()
        board_item['board_title'] = response.xpath('/html/body/div[2]/div[1]/div/b[3]/a/text()').extract_first()
        board_item['board_link'] = response.xpath('/html/body/div[2]/div[1]/div/b[3]/a/@href').extract_first()
        urls_found = response.xpath('*//a/@href').extract()
        bitcointalk_urls_found = [x for x in urls_found if 'bitcointalk' in x]
        board_item['board_urls'] = bitcointalk_urls_found
        for url in bitcointalk_urls_found:
            yield Request(url, callback=self.parse_item, dont_filter=False)
        # yield board_item

    def parse_topic(self, response):
        today = datetime.now()
        today_str = today.strftime("%d/%m/%Y")
        post_items = PostItem()
        # post_items['topic_page_html'] = str(response.body)
        post_items['board_title'] = response.xpath('//*[@id="bodyarea"]/div[1]/div/b[3]/a/text()').extract_first()
        post_items['board_link'] = response.xpath('//*[@id="bodyarea"]/div[1]/div/b[3]/a/@href').extract_first()
        try:
            board_moderator = response.xpath('/html/body/div[2]/div[1]/div/a/text()').extract_first()
            post_items['board_moderator'] = board_moderator
            board_moderator_profile_link = response.xpath('/html/body/div[2]/div[1]/div/a/@href').extract_first()
            post_items['board_moderator_profile_link'] = board_moderator_profile_link
        except ValueError:
            post_items['board_moderator'] = None
            post_items['board_moderator_profile_link'] = None
        post_items['topic_title'] = response.xpath('/html/body/div/div/div/b[4]/a/text()').extract_first()
        post_items['topic_link'] = response.url
        topic_page_number = response.xpath(".//td[contains(@class, 'middletext')]/b/text()").extract()
        post_items['topic_page_number'] = topic_page_number[1]
        post_windows = response.xpath("//*[contains(@class, 'window')]")
        post = []
        for post_item in post_windows:
            d = {}
            __post_text__ = post_item.xpath(".//div[contains(@class,'post')]/text()").extract()
            if not __post_text__ or ' '.join(__post_text__) == 1522750019:
                continue
            else:
                d['post_text'] = ' '.join(__post_text__)
                message_count = post_item.xpath(".//div/a[contains(@class, 'message_number')]/text()").extract_first()
                message_date_xpath = post_item.xpath(".//*[contains(@valign, 'middle')]")
                message_date_html = message_date_xpath.xpath(".//div[contains(@class, 'smalltext')]").extract_first()
                date = BeautifulSoup(message_date_html, 'html.parser').text.replace(' at', '')
                try:
                    if 'Today' in date:
                        formatted_date = date.replace('Today', today_str)
                        formatted_date = datetime.strptime(formatted_date, "%d/%m/%Y %I:%M:%S %p")
                        d['message_date'] = formatted_date.strftime('%d/%m/%Y %H:%M:S')
                        d['message_date_time_stamp'] = int(time.mktime(formatted_date.timetuple()))
                    else:
                        formatted_date = datetime.strptime(date, "%B %d, %Y, %I:%M:%S %p")
                        d['message_date'] = formatted_date.strftime('%d/%m/%Y %H:%M:S')
                        d['message_date_time_stamp'] = int(time.mktime(formatted_date.timetuple()))
                except ValueError:
                    pass
                    d['message_count_in_post'] = int(message_count.strip('#'))
                message_link = post_item.xpath(".//div/a[contains(@class, 'message_number')]/@href").extract_first()
                d['message_link'] = message_link
                poster_username = post_item.xpath(".//td[contains(@class, 'poster_info')]/b/a/text()").extract_first()
                d['poster_username'] = poster_username
                poster_profile_url = post_item.xpath(".//td[contains(@class, 'poster_info')]/b/a/@href").extract_first()
                d['poster_profile_url'] = poster_profile_url
                yield Request(poster_profile_url, callback=self.parse_item, dont_filter=False)
                post.append(d)
        post_items['post'] = post
        yield post_items

    def parse_profile(self, response):
        profile_items = ProfileItem()
        profile_table = response.xpath(".//*[contains(@class, 'windowbg')]/table/tr")
        _user_name_ = response.xpath('.//title/text()').extract()
        if 'Error' in _user_name_:
            raise IgnoreRequest()
        profile_items['poster_username'] = _user_name_[0].split(' ')[len(_user_name_)-1]
        profile_items['poster_profile_url'] = response.url
        profile_items['poster_profile_id'] = response.url.split('=')[2]
        info = {}
        profile_object = []
        for row in profile_table:
            profile_info = row.xpath('.//text()').extract()
            filtered_profile_info = list(filter(lambda x: '\n\t' not in x, profile_info))
            if not filtered_profile_info:
                continue
            elif len(filtered_profile_info) == 1:
                key_ = filtered_profile_info[0]
                key_ = key_.replace(':', '')
                key_ = key_.replace(' ', '')
                info[key_] = None
            else:
                key_ = filtered_profile_info[0]
                key_ = key_.replace(':', '')
                key_ = key_.replace(' ', '')
                info[key_] = ' '.join(filtered_profile_info[1:])
        profile_object.append(info)
        profile_items['profile_object'] = profile_object
        yield profile_items

    def parse_item(self, response):
        if 'topic' in response.url:
            return self.parse_topic(response)
        if 'board' in response.url:
            return self.parse_board(response)
        if 'profile' in response.url:
            return self.parse_profile(response)
