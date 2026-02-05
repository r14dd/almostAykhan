SEED_URLS = [
    "https://abb-bank.az/az",
    "https://abb-bank.az/az/ferdi",
    "https://abb-bank.az/az/biznes",
    "https://abb-bank.az/az/kreditler",
    "https://abb-bank.az/az/kartlar",
    "https://abb-bank.az/az/emanetler",
    "https://abb-bank.az/az/haqqimizda",
]

ALLOWED_DOMAINS = {
    "abb-bank.az",
    "www.abb-bank.az",
}

MAX_CRAWL_DEPTH = 4
MAX_PAGES = 300


REQUEST_TIMEOUT = 10
MAX_RETRIES = 3
# CRAWL_DELAY_SECONDS = 0.3
CRAWL_DELAY_SECONDS = 0.5
MIN_CLEAN_TEXT_LEN = 150
CHUNKS_OUTPUT = "scraper/output/abb_chunks.json"



# User needs to be able to request info in all three
# Example: https://abb-bank.az/ru/biznes/mikro-biznes/gundelik-bankciliq

ALLOWED_PATH_PREFIXES = (
    "/az",
    "/en",
    "/ru",
    # "/az/",
    # "/en/",
    # "/ru/",
)


SUPPORTED_LANGUAGES = ("az", "en", "ru")

DISALLOWED_PATH_KEYWORDS = (
    "/assets/",
    "/media/",
    "/uploads/",
)

ALLOWED_CONTENT_TYPES = (
    "text/html",
)

HEADERS = {
    "User-Agent": "almostAykhan/1.0"
}



