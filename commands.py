import os
import click

from willcrawler.dao import es_object


@click.group()
def cli():
    pass


@cli.command()
@click.option("--url", "url", required=True, help="Elasticsearch index server address")
@click.option("--pages", "pages", type=int, default=2, help="Pages to scrap for each session")
def scrap(url, pages):
    original_environ = os.environ.copy()
    try:
        if pages == -1 or (pages > 0 and pages <= 5):
            os.environ["ES_URL"] = url
            os.environ["TOTAL_PAGES"] = str(pages)
            es_object.connection
            os.system("scrapy crawl asossessions")
            os.system("scrapy crawl asosproducts")
        else:
            raise ValueError("--pages must be -1 or between 1 and 5 (inclusive).")

    except Exception as e:
        print("The following exception happened: %s" % e)
        print("Please check the arguments and try again.")
    finally:
        os.environ.clear()
        os.environ.update(original_environ)


if __name__ == "__main__":
    cli()
