#! /usr/bin/python3
import sys
from datetime import datetime as dt
from datetime import timedelta
import subprocess
from definitions import SCRAPY_PATH, SCRAPY_CRAWLERS_PATH


print("Starting the script...")
out = subprocess.run([SCRAPY_PATH, 'crawl', 'ebay_check'], cwd=SCRAPY_CRAWLERS_PATH)
print("The exit code was: %d" % out.returncode)
