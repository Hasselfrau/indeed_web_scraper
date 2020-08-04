# import sqlite3
import os
import contextlib
import random
from datetime import datetime
import pymysql.cursors
from pymysql.cursors import DictCursorMixin, Cursor
from collections import OrderedDict
from conf import *

DATABASE = 'jobs'

class OrderedDictCursor(DictCursorMixin, Cursor):
    dict_type = OrderedDict


def create_db():

    connection = pymysql.connect(host=HOST,
                                 user=USER,
                                 password=DB_PASS,
                                 charset=CHARSET,
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor(OrderedDictCursor) as cur:
        sql_query = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '" + DATABASE + "';"
        cur.execute(sql_query)
        result = cur.fetchall()

    if len(result) > 0 and result[0]['SCHEMA_NAME'] == DATABASE:
        return

    with connection.cursor(OrderedDictCursor) as cur:
        sql_query = "CREATE DATABASE " + DATABASE + ";"
        cur.execute(sql_query)

        sql_query = "USE " + DATABASE + ";"
        cur.execute(sql_query)

    with connection.cursor(OrderedDictCursor) as cur:
        sql_query = '''
                CREATE TABLE companies (
                      company_id INT AUTO_INCREMENT PRIMARY KEY,
                      name TEXT,
                      activity_level TEXT
                    );
            '''
        cur.execute(sql_query)

    with connection.cursor(OrderedDictCursor) as cur:
        sql_query = '''
                 CREATE TABLE job_postings (
                       posting_id INT AUTO_INCREMENT PRIMARY KEY,
                       title VARCHAR(256),
                       location TEXT,
                       company_id INT,
                       salary TEXT,
                       synopsis TEXT,
                       description TEXT,
                       url_indeed VARCHAR(512),
                       url_publisher TEXT,
                       publish_date TEXT,
                       close_date TEXT,
                       record_added TEXT,
                       FOREIGN KEY (company_id) REFERENCES companies (company_id),
                       UNIQUE (url_indeed)
                     );
             '''
        cur.execute(sql_query)

    return

def add_records(batch, logger):

    connection = pymysql.connect(host=HOST,
                                 user=USER,
                                 password=DB_PASS,
                                 charset=CHARSET,
                                 cursorclass=pymysql.cursors.DictCursor)

    with connection.cursor(OrderedDictCursor) as cur:
        sql_query = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '" + DATABASE + "';"
        cur.execute(sql_query)
        result = cur.fetchall()

    if len(result) == 0:
        create_db()


    connection = pymysql.connect(host=HOST,
                                 user=USER,
                                 password=DB_PASS,
                                 db=DB_NAME,
                                 charset=CHARSET,
                                 cursorclass=pymysql.cursors.DictCursor)

    logger.info('Adding data to the database')

    with connection.cursor(OrderedDictCursor) as cur:

        sql_query = "USE " + DATABASE + ";"
        cur.execute(sql_query)

        for index, row in batch.iterrows():

            try:
                sql_query = "SELECT company_id FROM companies WHERE name = '" + str(row[2]) +"'"
                cur.execute(sql_query)
                company_id = cur.fetchall()[0]['company_id']
            except:
                sql_query = """
                        INSERT IGNORE INTO companies (name) VALUES (%s);
                        """
                cur.execute(sql_query, [str(row[2])])

                sql_query = "SELECT company_id FROM companies WHERE name = '" + str(row[2]) +"'"
                cur.execute(sql_query)
                company_id = cur.fetchall()[0]['company_id']

            record_added = str(datetime.now(tz=None))
            record_postings = [str(row[0])[:256],   # title
                               str(row[1]),         # location
                               company_id,
                               str(row[3]),         # salary
                               str(row[4]),         # synopsis
                               str(row[5]),         # job description
                               str(row[6])[:512],   # url_indeed
                               str(row[7]),         # url_publisher
                               str(row[8]),         # publish_date
                               record_added]
            try:
                sql_query = """
                        INSERT IGNORE INTO job_postings (title, location, company_id, salary, synopsis, description,
                                                         url_indeed, url_publisher, publish_date,
                                                         record_added)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                        """
                cur.execute(sql_query, record_postings)
            except Exception as e:
                logger.error(f'Warning: {str(e)}')



            cur.execute('''
                    SELECT COUNT(posting_id)
                    FROM job_postings
                    ''')
            curr_amount = cur.fetchall()[0]['COUNT(posting_id)']

        connection.commit()

    logger.info(f'{len(batch)} new job positions has been added to the database')
    logger.info(f'Current number of positions: {curr_amount}')



# import logging
# import pandas as pd
#
# LOG_NAME = 'scraper_log'
#
# logger = logging.getLogger(LOG_NAME)
# logger.setLevel(logging.INFO)
#
# df = pd.read_csv('result.csv')
# add_records(df, logger)