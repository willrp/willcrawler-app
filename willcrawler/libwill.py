import collections
import re
import os
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch


ELASTIC_HOST = os.getenv("ELASTIC_HOST")


def counter():
    value = 0

    def count(op):
        nonlocal value
        if op == "add":
            value += 1
        elif op == "sub":
            value -= 1
        elif op == "get":
            return value

    return count


def getByPos(lst):
    gen = (i for i, x in enumerate(lst) if re.search("\s+by+\s+", x))
    for i in gen:
        p = i + 1
        tb = re.split("\s+by+\s+", ' '.join(lst[:p]))
        kind = tb[0].strip(" -.")
        brand = tb[1].strip(" -.")
        details = [e for e in lst[p:] if not re.match("^[\s]+$", e)]
        return collections.namedtuple('kindbrand', 'kind, brand, details')(kind, brand, details)


def stripSpaces(str):
    return re.sub(r'[^\x00-\x7F]+', '', str).strip()


def get_session_id(esindex, estype, name, gender):
    esconn = Elasticsearch(ELASTIC_HOST)
    s = Search(using=esconn, index=esindex, doc_type=estype)
    s = s.filter("term", gender=gender.lower()).query("match_phrase", name=stripSpaces(str(name)).title())
    response = s.execute()
    try:
        hit = response.hits[0]
        return hit.meta.id
    except IndexError:
        return None
