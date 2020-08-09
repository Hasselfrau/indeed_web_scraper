import random
from time import sleep
import pandas as pd
import sys
import math

# internal module with own functions
import tools
import db_manager

BASE_URL = "https://www.indeed.com/jobs?q=data+scientist+%2420%2C000&l=New+York&start="
START_PAGE = 10
STEP = 10


def parse_pages(base_url, final_page):
    df_result = pd.DataFrame(columns=["Title", "Location", "Company", "Salary", "Synopsis", "Description",
                                      "URL_indeed", "URL_publisher", "Publish_date"])

    for suffix in range(START_PAGE, final_page, STEP):
        df_curr = tools.parse_list_of_jobs(base_url + str(suffix))
        df_result = pd.concat([df_result, df_curr], ignore_index=True)
        sleep(random.uniform(1, 3))

    df_result.to_csv('result.csv')

    # TODO: invoke function to append df to the database
    db_manager.add_records(df_result)

    return df_result


def usage():
    print('usage: multiple_job_parse.py <depth> ')
    print('<depth> is number of pages to parse; each page typically consists of 10 job positions')
    print('<depth> must be more than 10 and less or equal to 50 pages currently')
    print('number of pages will be rounded to the nearest ten')


def main():
    args = sys.argv[1:]

    if not args or len(args) > 1:
        # run module for testing purposes
        df_res = parse_pages(BASE_URL, 11)
        print(df_res)

        # usage()
        # sys.exit(1)

    try:
        depth = int(args[0])
    except:
        print('<depth> must be an integer')
        usage()
        sys.exit(1)

    if depth <= 50:
        final_page = int(math.ceil(depth / 10.0)) * 10  # round up to the nearest ten
        df_res = parse_pages(BASE_URL, final_page)
        print(df_res)

    elif depth <= 10 or depth > 50:
        print('please provide number more than 10 and less or equal to 50')
        usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
