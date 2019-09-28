from elasticsearch_dsl import DocType, Text, Keyword, Nested, Float


class Products(DocType):
    about = Text(fields={"keyword": Keyword()}, required=True)
    brand = Text(fields={"keyword": Keyword()}, required=True)
    care = Text(fields={"keyword": Keyword()}, required=True)
    code = Text(fields={"keyword": Keyword()}, required=True)
    details = Text(fields={"keyword": Keyword()}, required=True)
    gender = Text(fields={"keyword": Keyword()}, required=True)
    images = Text(fields={"keyword": Keyword()}, required=True)
    kind = Text(fields={"keyword": Keyword()}, required=True)
    link = Text(fields={"keyword": Keyword()}, required=True)
    name = Text(fields={"keyword": Keyword()}, required=True)
    price = Nested(
        properties={
            "currency": Text(fields={'keyword': Keyword()}, required=True),
            "outlet": Float(required=True),
            "retail": Float(required=True)
        }
    )
    sessionid = Text(fields={"keyword": Keyword()}, required=True)
    sessionname = Text(fields={"keyword": Keyword()}, required=True)
    storename = Text(fields={"keyword": Keyword()}, required=True)

    class Meta:
        index = "store"
        type = "products"
        doc_type = "products"
