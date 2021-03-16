# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from .db import db
from scrapy.exceptions import DropItem
import json
import requests
from .definitions import SLACK_WEBHOOK_URL
from datetime import datetime as dt
from datetime import timedelta


class EbayCheckListingPipeline:
    def open_spider(self, spider):
        spider.website_id = db.get_website_id(spider.allowed_domains[0])
        spider.ebay_listings = db.get_listings(spider.website_id)

    def process_item(self, item, spider):
        if self.check_for_update(item["Listing Time"]):
            db.add_listings(spider.website_id, item["Title"].replace("'", "''"))
            spider.logger.info(f'Adding Listing {item["Title"]} to DB. Sending Slack Message')
            self.send_msg_to_slack(item["Link"])
        else:
            spider.logger.debug(f'Listing already present in DB.')
            raise DropItem()
        return item

    def send_msg_to_slack(self, msg_data):
        webhook_url = SLACK_WEBHOOK_URL
        slack_data = {'text': f"A New Listing is available: {msg_data} \n"}
        response = requests.post(webhook_url, data=json.dumps(slack_data), headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )

    def check_for_update(self, item_date):
        item_date = item_date + " " + str(dt.now().year)
        item_date_obj = dt.strptime(item_date, "%d-%b %H:%M %Y")
        time_previous = dt.now() - timedelta(minutes=70)
        if item_date_obj > time_previous:
            return True

