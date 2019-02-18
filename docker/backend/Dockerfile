FROM python:3.6-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get -qq update \
    && apt-get -qq -y install \
        libpq-dev \
        gcc \
        vim \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -qq -y clean


COPY ./docker/backend/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
    && chmod +x /entrypoint.sh

COPY ./docker/backend/start.sh /start.sh
RUN sed -i 's/\r//' /start.sh \
    && chmod +x /start.sh

COPY ./backend/requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt \
    && rm /requirements.txt

COPY ./backend/ /app
WORKDIR /app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/start.sh"]
