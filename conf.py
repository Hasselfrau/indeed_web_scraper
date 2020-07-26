BASE_URL = "https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start="
ROOT_URL = "https://www.indeed.com"
START_PAGE = 10
STEP = 10
LOWER_BOUND = 10
UPPER_BOUND = 50
COLUMNS = ["Title", "Location", "Company", "Salary", "Synopsis", "Description",
                               "URL_indeed", "URL_publisher", "Publish_date"]

HEADERS = {
        'User-Agent': 'My User Agent 1.0',
        'From': 'youremail@domain.com'
    }

LOG_NAME = 'scraper_log'
LOG_INFO = '>>>>> Start scrapping <<<<<'
