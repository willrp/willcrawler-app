import json
import re
import os

import scrapy
from scrapy.loader import ItemLoader

from willcrawler.items import AsosSession, AsosProduct, AsosPrice
from willcrawler.libwill import getByPos, stripSpaces, get_session_id


class AsosSessions(scrapy.Spider):
    name = "asossessions"
    user_agent = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    download_delay = 0.5
    start_urls = [
        "http://www.asos.com/women/sale/",
        "http://www.asos.com/men/sale/"
    ]
    storename = "asos"

    custom_settings = {
        "ELASTICSEARCH_INDEX": "store",
        "ELASTICSEARCH_TYPE": "sessions"
    }

    pos = 0

    def parse(self, response):
        sessions = response.css("article.feature")
        for session in sessions:
            lsession = ItemLoader(item=AsosSession(), response=response)
            name = "".join(session.css("div.feature__title h3::text").extract())
            gender = re.split("[/]+", response.request.url)[2]
            image = str(session.css("div.feature__image img::attr(data-src)").extract_first()).split("?")[0]

            lsession.add_value("pos", self.pos)
            lsession.add_value("name", stripSpaces(str(name).title()))
            lsession.add_value("gender", stripSpaces(str(gender).title()))
            lsession.add_value("image", stripSpaces(str(image)))
            lsession.add_value("storename", self.storename.title())

            self.pos += 1
            yield lsession.load_item()


class AsosProducts(scrapy.Spider):
    name = "asosproducts"
    user_agent = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    download_delay = 0.5
    start_urls = [
        "http://www.asos.com/women/sale/",
        "http://www.asos.com/men/sale/"
    ]
    baseurl = "http://asos.com"
    imgwidth = 500
    storename = "asos"

    custom_settings = {
        "ELASTICSEARCH_INDEX": "store",
        "ELASTICSEARCH_TYPE": "products"
    }

    def parse(self, response):
        sessions = response.css("article.feature")
        for session in sessions:
            sessionname = "".join(session.css("div.feature__title h3::text").extract())
            gender = re.split("[/]+", response.request.url)[2]
            sessionlink = session.css("a.feature__link::attr(href)").extract_first()

            esindex = "store"
            estype = "sessions"
            sessionid = get_session_id(esindex, estype, sessionname, gender)

            requestsession = response.follow(sessionlink, callback=self.parse_session)
            requestsession.meta["sessionid"] = sessionid
            requestsession.meta["sessionname"] = sessionname
            requestsession.meta["gender"] = gender
            requestsession.meta["pages"] = 1
            yield requestsession

    def parse_session(self, response):
        sessionid = response.meta["sessionid"]
        sessionname = response.meta["sessionname"]
        gender = response.meta["gender"]
        pages = response.meta["pages"]

        products = response.css("li.product-container")

        for product in products:
            productlink = product.css("a.product-link::attr(href)").extract_first()
            requestproduct = response.follow(productlink, callback=self.parse_product)
            requestproduct.meta["sessionid"] = sessionid
            requestproduct.meta["sessionname"] = sessionname
            requestproduct.meta["gender"] = gender
            requestproduct.meta["productlink"] = productlink
            yield requestproduct

        nextpage = response.css("ul.pager li.next a::attr(href)").extract_first()

        total_pages = int(os.getenv("TOTAL_PAGES"))

        if pages < total_pages or total_pages == -1:
            pages += 1
            requestnewpage = response.follow(nextpage, callback=self.parse_session)
            requestnewpage.meta["sessionid"] = sessionid
            requestnewpage.meta["sessionname"] = sessionname
            requestnewpage.meta["gender"] = gender
            requestnewpage.meta["pages"] = pages
            yield requestnewpage

    def parse_product(self, response):
        try:
            sessionid = response.meta["sessionid"]
            sessionname = response.meta["sessionname"]
            gender = response.meta["gender"]
            productlink = response.meta["productlink"]

            lproduct = ItemLoader(item=AsosProduct(), response=response)

            name = response.css("div.product-hero>h1::text").extract_first()
            code = response.css("div.product-code>span::text").extract_first()
            kind = response.css("div.product-description span strong:nth-child(1)::text").extract_first()
            brand = response.css("div.brand-description span strong::text").extract_first()
            details = response.css("div.product-description span ul>li::text").extract()

            # FIXING DISCREPANCIES ON ASOS STORE WEBPAGE STRUCTURE
            if (kind is None) or (brand is None):
                temp = getByPos(details)
                details = temp.details
                if (kind is None) or (kind == " "):
                    kind = temp.kind
                if brand is None:
                    brand = temp.brand
            # FURTHER FIXING WITH PARISIAN PETITE BRAND
            if re.search("\s+$", str(kind)) is not None:
                kind = str(kind) + str(response.css("div.product-description span a>strong::text").extract_first())

            care = response.css("div.care-info span::text").extract_first()

            # FIXING DISCREPANCIES ON ASOS STORE WEBPAGE STRUCTURE ON CARE SECTION
            if care is None:
                care = response.css("div.care-info span>*::text").extract_first()

            lstimages = response.css("div.product-gallery li.image-thumbnail img::attr(src)").extract()
            images = [(img.split("?", 1)[0] + "?wid=" + str(self.imgwidth)) for img in lstimages]

            about = response.css("div.about-me span::text").extract_first()

            # FIXING DISCREPANCIES ON ASOS STORE WEBPAGE STRUCTURE ON ABOUT SECTION
            if about is None:
                about = response.css("div.about-me span>*::text").extract_first()

            # Todo: GETTING ONLY RELIABLE DATA IN ORDER TO DEPLOY
            if name is None:
                raise AttributeError("No name")
            elif code is None:
                raise AttributeError("No code")
            elif productlink is None:
                raise AttributeError("No product link")
            elif kind is None:
                raise AttributeError("No kind")
            elif brand is None:
                raise AttributeError("No brand")
            elif details is None:
                raise AttributeError("No details")
            elif care is None:
                raise AttributeError("No care")
            elif about is None:
                raise AttributeError("No about")
            elif images is None:
                raise AttributeError("No images")

            lproduct.replace_value("name", stripSpaces(str(name)).title())
            lproduct.replace_value("code", stripSpaces(str(code)))
            lproduct.replace_value("link", stripSpaces(str(productlink)))
            lproduct.replace_value("kind", stripSpaces(str(kind)).title())
            lproduct.replace_value("brand", stripSpaces(str(brand)).title())
            lproduct.replace_value("details", [str(x).strip() for x in details])
            lproduct.replace_value("care", stripSpaces(str(care)))
            lproduct.replace_value("about", stripSpaces(str(about)))
            lproduct.replace_value("images", images)
            lproduct.replace_value("storename", self.storename.title())
            lproduct.replace_value("sessionid", str(sessionid))
            lproduct.replace_value("sessionname", stripSpaces(str(sessionname)).title())
            lproduct.replace_value("gender", stripSpaces(str(gender)).title())

            iid = re.findall("iid=[0-9]+", productlink)[0][4:]
            pricelink = "http://www.asos.com/api/product/catalogue/v2/stockprice?" \
                        "productIds=" + iid + "&store=COM&currency=GBP"

            requestprice = response.follow(pricelink, callback=self.parse_price)
            requestprice.meta["lproduct"] = lproduct

            yield requestprice
        # Exception for products that have other products inside, like suits and vests
        except AttributeError as e:
            self.logger.info(str(e))

    def parse_price(self, response):
        try:
            lproduct = response.meta["lproduct"]

            lprice = ItemLoader(item=AsosPrice(), response=response)

            pricejson = json.loads(response.body)
            outletprice = pricejson[0]["productPrice"]["current"]["value"]
            if str(outletprice) == "0.0":
                outletprice = pricejson[0]["productPrice"]["xrp"]["value"]
            retailprice = pricejson[0]["productPrice"]["rrp"]["value"]
            if str(retailprice) == "0.0":
                retailprice = pricejson[0]["productPrice"]["previous"]["value"]

            currency = pricejson[0]["productPrice"]["currency"]

            lprice.replace_value("outlet", float(outletprice))
            lprice.replace_value("retail", float(retailprice))
            lprice.replace_value("currency", str(currency).upper())
            lproduct.replace_value("price", dict(lprice.load_item()))
            yield lproduct.load_item()
        # Exception for products that have other products inside, like suits and vests
        except AttributeError as e:
            self.logger.info(str(e))
