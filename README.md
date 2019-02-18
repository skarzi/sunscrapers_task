# Sunscrapers task

Recruitment Task from Sunscrapers.

To run this project **docker** and **docker-compose** are required.

## Getting started

### Running "production" version

This is rather "development" version :)

```bash
cp .env.sample .env
docker-compose up --build -d
```


## Project Architecture

Projects consists of 2 microservices: `scrapers` and `api`.

### Scrapers microservice

Responsible for scraping rates date from
[ecb.europa.eu](https://www.ecb.europa.eu/home/html/rss.en.html).

This service is built using [Scrapy](https://github.com/scrapy/scrapy/).
Cron is used to schedule scraping tasks.
By default scraping is run each 6 hours.

Scrapping works in following way:

+ extract Euro foreign exchange reference rates RSS links from main page
+ follow them and extract rates data from xml feeds
+ constantly POST extracted rates data to rates REST API

#### Running scraping by hand

This should be done before getting latest rates from API in development mode.

```bash
docker-compose run --rm scrapers bash /app/run_scrapers.sh
```

#### Improvements

More detailed improvements propositions are written in `scrapers` directory.

+ add tests using previously recorded HTTP interaction
  with tools like [VCR](https://github.com/vcr/vcr)
  or [betamax](https://github.com/betamaxpy/betamax)
+ more efficient items saving - look at TODO comment in
 `scrapers/ecb/pipelines.py`
+ dynamic extraction of scraping frequency
+ dynamic extraction of XML feed namespaces


### REST API microservice

Provide `Create` and `Read` (only list latest rates) actions for rates data.
Caching of rates list responses is used with
[redis](https://github.com/antirez/redis) based cache.

This service is built using [Django](https://github.com/django/django/)
with [Django Rest Framework](https://github.com/encode/django-rest-framework/).
Unit tests are written using [pytest](https://github.com/pytest-dev/pytest)
and [factory boy](https://github.com/FactoryBoy/factory_boy).

#### Running tests

```bash
docker-compose run --rm api pytest
```

#### Improvements

+ better rates model schema - I was running out of time so I didn't have time
  to design better schema or use time series database, for instance
  [influxdb](https://github.com/influxdata/influxdb), which is probably the
  best choice for working with such data (maybe more frequent but still :)
+ add other endpoints, for instance for getting history of requested
  currency or batch create
+ add filters, for instance for getting rates from given datetime - in current
  version it's impossible, because of lack of time I used `RawQuerySet`.
+ add pagination for list responses
+ add more tests
+ split requirements by environment
+ wrap list responses into some namespace, for instance `{"data": [...]}` -
  this will allow to add some metadata to list responses, but also prevent
  JSON Hijacking
