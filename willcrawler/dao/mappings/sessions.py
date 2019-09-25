from elasticsearch_dsl import DocType, Text, Keyword, Long


class Sessions(DocType):
    gender = Text(fields={"keyword": Keyword()})
    image = Text(fields={"keyword": Keyword()})
    name = Text(fields={"keyword": Keyword()})
    pos = Long()
    storename = Text(fields={"keyword": Keyword()})

    class Meta:
        index = "store"
        type = "sessions"
        doc_type = "sessions"
