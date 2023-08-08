# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class GetyourguideScrapyItem_LV(scrapy.Item):
    activity_name = scrapy.Field()
    activity_type = scrapy.Field()
    activity_additional_data = scrapy.Field()
    activity_rating = scrapy.Field()
    total_reviews = scrapy.Field()
    activity_price = scrapy.Field()
    activity_url = scrapy.Field()
    pass

class GetyourguideScrapyItem_PV(scrapy.Item):
    activity_overview = scrapy.Field()
    activity_details = scrapy.Field()
    activity_description = scrapy.Field()
    activity_experience = scrapy.Field()
    activity_meeting_point = scrapy.Field()
    activity_important_information = scrapy.Field()
    activity_review_summary = scrapy.Field()
    activity_includes = scrapy.Field()
    activity_not_includes = scrapy.Field()
    activity_provider = scrapy.Field()
    activity_not_suitable_for = scrapy.Field()
    pass