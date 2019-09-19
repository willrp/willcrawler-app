from scrapy.item import Item, Field
from scrapy.loader.processors import TakeFirst


class AsosSession(Item):
    pos = Field(
        output_processor=TakeFirst()
    )
    name = Field(
        output_processor=TakeFirst()
    )
    gender = Field(
        output_processor=TakeFirst()
    )
    image = Field(
        output_processor=TakeFirst()
    )
    storename = Field(
        output_processor=TakeFirst()
    )


class AsosPrice(Item):
    retail = Field(
        output_processor=TakeFirst()
    )
    outlet = Field(
        output_processor=TakeFirst()
    )
    currency = Field(
        output_processor=TakeFirst()
    )


class AsosProduct(Item):
    name = Field(
        output_processor=TakeFirst()
    )
    code = Field(
        output_processor=TakeFirst()
    )
    link = Field(
        output_processor=TakeFirst()
    )
    kind = Field(
        output_processor=TakeFirst()
    )
    brand = Field(
        output_processor=TakeFirst()
    )
    details = Field()
    care = Field(
        output_processor=TakeFirst()
    )
    price = Field(
        output_processor=TakeFirst(),
        serializer=AsosPrice
    )
    about = Field(
        output_processor=TakeFirst()
    )
    images = Field()
    storename = Field(
        output_processor=TakeFirst()
    )
    sessionid = Field(
        output_processor=TakeFirst()
    )
    sessionname = Field(
        output_processor=TakeFirst()
    )
    gender = Field(
        output_processor=TakeFirst()
    )
