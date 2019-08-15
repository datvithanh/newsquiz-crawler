import scrapy
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from newsquiz.spiders.evnexpress import EvnexpressBusinessSpider, EvnexpressTravelSpider, EvnexpressSportsSpider, EvnexpressLifeSpider
from newsquiz.spiders.urbanisthanoi import UrbanisthanoiArtsCultureSpider, UrbanisthanoiEatDrinkSpider, UrbanisthanoiNewsSpider, UrbanisthanoiSocietySpider,UrbanisthanoiOldHanoiSpider
from newsquiz.spiders.vietnamnews import VietnamnewsPoliticsLawsSpider, VietnamnewsSocietySpider, VietnamnewsEconomySpider, VietnamnewsLifestyleSpider, VietnamnewsSportsSpider, VietnamnewsEnvironmentSpider
from newsquiz.spiders.kpop import KpopSpider

clses = [EvnexpressBusinessSpider, EvnexpressTravelSpider, EvnexpressSportsSpider, EvnexpressLifeSpider, UrbanisthanoiArtsCultureSpider, UrbanisthanoiEatDrinkSpider, UrbanisthanoiNewsSpider, UrbanisthanoiSocietySpider, UrbanisthanoiOldHanoiSpider, VietnamnewsPoliticsLawsSpider, VietnamnewsSocietySpider, VietnamnewsEconomySpider, VietnamnewsLifestyleSpider, VietnamnewsSportsSpider, VietnamnewsEnvironmentSpider, KpopSpider]
clses = [UrbanisthanoiArtsCultureSpider, UrbanisthanoiEatDrinkSpider, UrbanisthanoiNewsSpider, UrbanisthanoiOldHanoiSpider, UrbanisthanoiSocietySpider]

configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    for cl in clses:
        yield runner.crawl(cl)
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished