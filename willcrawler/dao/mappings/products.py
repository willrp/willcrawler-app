from elasticsearch_dsl import DocType, Text, Keyword, Nested, Float


class Products(DocType):
    about = Text(fields={"keyword": Keyword()})
    brand = Text(fields={"keyword": Keyword()})
    care = Text(fields={"keyword": Keyword()})
    code = Text(fields={"keyword": Keyword()})
    details = Text(fields={"keyword": Keyword()})
    gender = Text(fields={"keyword": Keyword()})
    images = Text(fields={"keyword": Keyword()})
    kind = Text(fields={"keyword": Keyword()})
    link = Text(fields={"keyword": Keyword()})
    name = Text(fields={"keyword": Keyword()})
    price = Nested(
        properties={
            "currency": Text(fields={'keyword': Keyword()}),
            "outlet": Float(),
            "retail": Float()
        }
    )
    sessionid = Text(fields={"keyword": Keyword()})
    sessionname = Text(fields={"keyword": Keyword()})
    storename = Text(fields={"keyword": Keyword()})

    class Meta:
        index = "store"
        type = "products"
        doc_type = "products"
