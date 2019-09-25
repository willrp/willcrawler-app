import os

ES_URL = os.getenv("ES_URL")

BOT_NAME = "willcrawler"
SPIDER_MODULES = ["willcrawler.spiders"]
NEWSPIDER_MODULE = "willcrawler.spiders"
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 500
}

ELASTICSEARCH_SERVERS = [ES_URL]
LOG_FILE = "willcrawler.log"
LOG_ENABLED = True
