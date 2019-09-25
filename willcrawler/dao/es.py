import os
from elasticsearch import Elasticsearch

from .mappings import Products, Sessions


class ES(object):
    def __init__(self) -> None:
        self.__conn = None

    @property
    def connection(self):
        if(self.__conn is None):
            self.__conn = Elasticsearch(os.getenv("ES_URL"))
            Sessions.init(using=self.__conn)
            Products.init(using=self.__conn)
        return self.__conn
