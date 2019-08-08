from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from newsquiz.spiders.evnexpress import EvnexpressBusinessSpider, EvnexpressTravelSpider, EvnexpressSportsSpider, EvnexpressLifeSpider
from newsquiz.spiders.urbanisthanoi import UrbanisthanoiArtsCultureSpider, UrbanisthanoiEatDrinkSpider, UrbanisthanoiNewsSpider, UrbanisthanoiSocietySpider, UrbanisthanoiSocietySpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

clses = [EvnexpressBusinessSpider, EvnexpressTravelSpider, EvnexpressSportsSpider, EvnexpressLifeSpider, UrbanisthanoiArtsCultureSpider, UrbanisthanoiEatDrinkSpider, UrbanisthanoiNewsSpider, UrbanisthanoiSocietySpider, UrbanisthanoiSocietySpider]

process = CrawlerProcess(get_project_settings())
for cl in clses:
    process.crawl(cl)

def sensor():
    process.start()

sched = BackgroundScheduler(daemon=True)
sched.add_job(sensor,'interval',minutes=10)
sched.start()

app = Flask(__name__)

@app.route("/home")
def home():
    """ Function for test purposes. """
    return "Welcome Home :) !"

if __name__ == "__main__":
    app.run()