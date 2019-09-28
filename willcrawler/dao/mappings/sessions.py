from elasticsearch_dsl import DocType, Text, Keyword, Long


class Sessions(DocType):
    gender = Text(fields={"keyword": Keyword()}, required=True)
    image = Text(fields={"keyword": Keyword()}, required=True)
    name = Text(fields={"keyword": Keyword()}, required=True)
    pos = Long(required=True)
    storename = Text(fields={"keyword": Keyword()}, required=True)

    class Meta:
        index = "store"
        type = "sessions"
        doc_type = "sessions"
