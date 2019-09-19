import os
import click
import json
import requests


@click.group()
def cli():
    pass


@cli.command()
@click.option("--url", "url", required=True, help="Elasticsearch index server address")
def mapping(url):
    """Create mapping on Elasticsearch database"""
    try:
        print("Creating map on index: %s/store" % url)
        response = requests.get(
            url + "/store/_mapping"
        )

        if response.status_code == 404:
            print("Mapping not found, creating a new one.")
            with open("mapping.json") as f:
                data = json.loads(f.read())
                f.close()

                response = requests.put(
                    url + "/store",
                    json=data
                )

                response.raise_for_status()
                print("Mapping created successfully.")
        else:
            print("Mapping already exists, operation aborted.")
    except Exception as e:
        print("The following exception happened: %s" % e)
        print("Please check the --url argument and try again.")


@cli.command()
@click.option("--url", "url", required=True, help="Elasticsearch index server address")
@click.option("--pages", "pages", type=int, default=2, help="Pages to scrap for each session")
def scrap(url, pages):
    original_environ = os.environ.copy()
    try:
        if pages == -1 or (pages > 0 and pages <= 5):
            os.environ["ELASTIC_HOST"] = url
            os.environ["TOTAL_PAGES"] = str(pages)
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
