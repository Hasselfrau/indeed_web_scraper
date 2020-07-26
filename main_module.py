import random
from time import sleep
import pandas as pd
import sys
import math
import argparse
import logging
from conf import *

# internal modules with own functions
import tools
import db_manager

def parse_pages(final_page):
    '''
    Generate a list with urls and put it into parser function
    Recieves dataframe from each link and append to general dataframe
    then upload it to database
    '''
    df_result = pd.DataFrame(columns=COLUMNS)

    urls = []
    for suffix in range(START_PAGE, final_page, STEP):
        urls.append(BASE_URL + str(suffix))
    df_curr = tools.greq_parse(urls, logger)
    df_result = pd.concat([df_result, df_curr], ignore_index=True)

    db_manager.add_records(df_result, logger)
    return


def usage():
    print('usage: main_module.py <depth>')
    print('<depth> is number of pages to parse; each page typically consists of 10 job positions')
    print(f'<depth> must be more or equal than {LOWER_BOUND} and less or equal than {UPPER_BOUND} pages currently')
    print('number of pages will be rounded to the nearest ten')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('x', type=int)
    try:
        args = parser.parse_args()
    except SystemExit as err:
        logger.error(f'Error code{err}.Function ran without parameter')
        usage()
        sys.exit(err)


    if LOWER_BOUND <= args.x <= UPPER_BOUND:
        final_page = int(math.ceil(args.x / 10.0)) * 10  # round up to the nearest ten
        logger.info(f'Set last page: {final_page}')
        parse_pages(final_page)

    else:
        logger.error(f'please provide number more than {LOWER_BOUND} and less or equal to {UPPER_BOUND}')
        usage()
        sys.exit(1)


if __name__ == '__main__':
    logger = logging.getLogger(LOG_NAME)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(f'{LOG_NAME}.log')
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    logger.info(LOG_INFO)
    main()
