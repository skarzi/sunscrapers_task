FROM python:3.6-slim

RUN apt-get -qq update \
     && apt-get -qq -y install \
        libpq-dev \
        gcc \
        libxml2-dev \
        libxslt1-dev \
        zlib1g-dev \
        libffi-dev \
        libssl-dev \
        cron \
     && rm -rf /var/lib/apt/lists/* \
     && apt-get -qq -y clean

COPY ./scrapers/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt \
    && rm /requirements.txt

COPY ./scrapers /app

ADD ./scrapers/crontab /etc/cron.d/scrapers
RUN chmod 0600 /etc/cron.d/scrapers
RUN touch /var/log/cron.log

WORKDIR /app

CMD cron && tail -f /var/log/cron.log
