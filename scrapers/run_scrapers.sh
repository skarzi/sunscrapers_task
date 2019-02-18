#!/bin/bash

cd /app/ || exit
PATH=$PATH:/usr/local/bin
export PATH
scrapy crawl ecb_europa
