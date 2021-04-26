import scrapy

from scrapy.loader import ItemLoader

from ..items import QiibqaItem
from itemloaders.processors import TakeFirst


class QiibqaSpider(scrapy.Spider):
	name = 'qiibqa'
	start_urls = ['https://www.qiib.com.qa/Press/List/News']

	def parse(self, response):
		post_links = response.xpath('//a[@class="read-more"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@rel="next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h2/text()').get()
		description = response.xpath('//section[@id="news-item"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="post-meta-date"]/a/text()').get()

		item = ItemLoader(item=QiibqaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
