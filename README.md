# WillCrawler APP

WillCrawler is an application to serve as data source for the WillBuyer demonstration project.

* The products web crawler, to crawl information from other stores;
* Scrapy project;
* Stores data into Elasticsearch;
* In order to bypass flaws on store view structure, makes verifications based on the observed patterns.

## Built With

* [Elasticsearch](https://www.elastic.co): A distributed, RESTful search and analytics engine. To store and search data;
* [Elasticsearch DSL](https://github.com/elastic/elasticsearch-dsl-py): A high-level library to write and run queries against Elasticsearch for Python;
* [Python](https://www.python.org): Main backend programming language. For Web services control, service and model layers;
* [Python-dotenv](https://github.com/theskumar/python-dotenv): Get and set values in your .env file in local and production servers;
* [Pip](https://pypi.python.org/pypi/pip): For dependency management of Python APIs, libraries and frameworks. Bundled with Python;
* [Pipenv](https://github.com/pypa/pipenv): Package manager for Python programming language;
* [Scrapy](https://scrapy.org): Web crawling framework. For crawling data from e-commerce webpages and structure it;
* [Scrapy-Elasticsearch](https://github.com/knockrentals/scrapy-elasticsearch): A Scrapy pipeline which send items to Elasticsearch server.

## Development tools

* [Click](https://github.com/pallets/click): Python composable command line interface toolkit;
* [Docker](https://www.docker.com/): Performs web services containerization, helping on application development, integration tests and production. Boosts production by getting everything started easily and isolated, and reloading the application on code change.

## Prerequisites

The following softwares are needed in order to install this application:

* [Python](https://www.python.org) >= 3.7.4;
* [Docker](https://www.docker.com/)
* [Elasticsearch](https://www.elastic.co/) == 5.4.3.

## Package manager - Pipenv

In order to develop different web services and modules, different environments is a must. They will have their own packages, libraries and variables, simulating the production environment. So here, we will use Pipenv to manage everything.

### Installation

To install it, open the command prompt, access the project folder and run:

```
$ pip install pipenv
```

### Install the project dependencies

In order to install all the project dependencies, including the development ones, run the following command:

```
$ pipenv install --dev
```

## Elasticsearch

The Elasticsearch server described in this guideline is for development. For production, please set up your own production server.

### Running the server

With your docker machine running, open the command prompt and run:

```
$ docker-compose up
```

The Elasticsearch server will run on port 9200. The IP address will be the same one as your Docker machine.

In order to get the IP of you Docker machine. In order to obtain it, open the command prompt and run:

```
$ docker-machine ip
```

The return value of this command will be referenced as DOCKER_MACHINE_IP. If you have your own production server, please replace with it's own IP address.

## Data crawling

This process needs an active Internet connection and **might take some time**. Locally, from 1 store, it may crawl thousands of products.

This step needs an Elasticsearch [server running](running-the-server). Access the [project folder](/) with the command prompt, and run the following command.

```
$ pipenv run python commands.py scrap --url http://DOCKER_MACHINE_IP:9200 --pages NUM_PAGES
```

Where NUM_PAGES is the number of pages that you want to scrap per session. Maximum is 5. Use the value -1 if you want to scrap all pages. The --pages argument is optional.

After the operation completes, a log will be available on the [project folder](/).

## Authors

Engineered and coded by:
* **Will Roger Pereira** - https://github.com/willrp

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
