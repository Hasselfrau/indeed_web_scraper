import sqlite3
import os
import contextlib
import random
from datetime import datetime

DB_FILENAME = 'jobs.db'

def create_db():
    if os.path.exists(DB_FILENAME):
        os.remove(DB_FILENAME)

    with contextlib.closing(sqlite3.connect(DB_FILENAME)) as con: # auto-closes
        with con: # auto-commits
            cur = con.cursor()

            sql_query = '''
                    CREATE TABLE job_postings (
                      posting_id int INTEGER PRIMARY KEY,
                      title TEXT,
                      location TEXT,
                      company_id INTEGER,
                      salary TEXT,
                      synopsis TEXT,
                      description TEXT,
                      url_indeed TEXT,
                      url_publisher TEXT,
                      publish_date TEXT,
                      close_date TEXT,
                      record_added TEXT,
                      FOREIGN KEY (company_id)
                      REFERENCES companies (company_id) 
                        ON UPDATE SET NULL
                        ON DELETE SET NULL
                      UNIQUE (title, synopsis)
                    );
                '''
            cur.execute(sql_query)

            sql_query = '''
                    CREATE TABLE companies (
                      company_id int INTEGER PRIMARY KEY,
                      name TEXT,
                      activity_level TEXT
                    );
                '''
            cur.execute(sql_query)

            # sql_query = '''
            #         CREATE TABLE requirements (
            #           req_id int INTEGER PRIMARY KEY,
            #           name TEXT,
            #           description TEXT,
            #           posting_id INTEGER,
            #           FOREIGN KEY (posting_id)
            #           REFERENCES job_postings (posting_id)
            #             ON UPDATE SET NULL
            #             ON DELETE SET NULL
            #         );
            #     '''
            # cur.execute(sql_query)

            con.commit()

    return


def add_records(batch):
    if not os.path.exists(DB_FILENAME):
        create_db()

    with contextlib.closing(sqlite3.connect(DB_FILENAME)) as con: # auto-closes
        with con: # auto-commits
            cur = con.cursor()

            # posting_id = 0
            for index, row in batch.iterrows():

                posting_id = random.randint(0, 10000000)
                company_id = random.randint(0, 10000000)
                record_added = str(datetime.now(tz=None))

                record = [posting_id, row[0], row[1], company_id, row[3],
                          row[4],row[5],row[6],row[7],row[8], "NULL", record_added]

                sql_query = """
                        INSERT OR IGNORE INTO job_postings (posting_id, title, location, company_id,
                        salary, synopsis, description, url_indeed, url_publisher,
                        publish_date, close_date, record_added) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """
                cur.execute(sql_query, record)

            con.commit()


if not os.path.exists(DB_FILENAME):
    create_db()
