# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field
from scrapy import Item


class PostItem(Item):
    # define the fields for your item here like:
    topic_page_html = Field()
    bitcoin_address = Field()
    bitcoin_transaction = Field()
    board_title = Field()
    board_link = Field()
    board_moderator = Field()
    board_moderator_profile_link = Field()
    topic_title = Field()
    topic_link = Field()
    post = Field()
    topic_page_number = Field()


class BoardItem(Item):
    board_title = Field()
    board_link = Field()
    board_urls = Field()


class ProfileItem(Item):
    poster_username = Field()
    poster_profile_url = Field()
    poster_profile_id = Field()
    profile_object = Field()
