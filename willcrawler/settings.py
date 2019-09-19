import os

ELASTIC_HOST = os.getenv("ELASTIC_HOST")

BOT_NAME = "willcrawler"
SPIDER_MODULES = ["willcrawler.spiders"]
NEWSPIDER_MODULE = "willcrawler.spiders"
ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
    'scrapyelasticsearch.scrapyelasticsearch.ElasticSearchPipeline': 500
}

ELASTICSEARCH_SERVERS = [ELASTIC_HOST]
LOG_FILE = "willcrawler.log"
LOG_ENABLED = True
