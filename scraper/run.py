import urllib.parse
import json
import datetime
import time
import hashlib
import requests
from bs4 import BeautifulSoup

SEED_URLS = "https://abb-bank.az/"

res = requests.get(SEED_URLS)

print(res.content)

print("status code: " + str(res.status_code))