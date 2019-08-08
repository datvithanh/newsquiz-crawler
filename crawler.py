from newsquiz.spiders.evnexpress import EvnexpressBusinessSpider, EvnexpressTravelSpider, EvnexpressSportsSpider, EvnexpressLifeSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

process.crawl(EvnexpressBusinessSpider)
process.crawl(EvnexpressTravelSpider)
process.crawl(EvnexpressSportsSpider)
process.crawl(EvnexpressLifeSpider)

process.start()