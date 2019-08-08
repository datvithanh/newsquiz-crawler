from newsquiz.spiders.evnexpress import EvnexpressBusinessSpider, EvnexpressTravelSpider, EvnexpressSportsSpider, EvnexpressLifeSpider
from newsquiz.spiders.urbanisthanoi import UrbanisthanoiArtsCultureSpider, UrbanisthanoiEatDrinkSpider, UrbanisthanoiNewsSpider, UrbanisthanoiSocietySpider, UrbanisthanoiSocietySpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


process = CrawlerProcess(get_project_settings())

process.crawl(UrbanisthanoiArtsCultureSpider)
process.crawl(UrbanisthanoiEatDrinkSpider)
# process.crawl(EvnexpressSportsSpider)
# process.crawl(EvnexpressLifeSpider)

process.start()