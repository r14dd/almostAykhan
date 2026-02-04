SEED_URL = "https://abb-bank.az/"

ALLOWED_DOMAINS = {
    "abb-bank.az",
    "www.abb-bank.az",
}
MAX_CRAWL_DEPTH = 5
MAX_PAGES = 1000
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3
CRAWL_DELAY_SECONDS = 0.5

RAW_OUTPUT = "./output/abb_pages.json"
CHUNKS_OUTPUT = "./output/abb_chunks.json"



# User needs to be able to request info in all three
# Example: https://abb-bank.az/ru/biznes/mikro-biznes/gundelik-bankciliq

ALLOWED_PATH_PREFIXES = (
    "/az",
    "/en",
    "/ru",
)


# unused for now
SUPPORTED_LANGUAGES = ("az", "en", "ru")


# We dont want all the media, files or auth info
DISALLOWED_PATH_KEYWORDS = (
    "/media/",
    "/assets/",
    "/uploads/",
    "/login",
    "/signin",
    "/auth",
    "/search",
    "/api/"
)

ALLOWED_CONTENT_TYPES = (
    "text/html",
)

HEADERS = {
    "User-Agent": "almostAykhan/1.0"
}




