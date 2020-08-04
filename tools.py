from gevent import monkey
monkey.patch_all()
import pandas as pd
from bs4 import BeautifulSoup
import requests
import grequests
import urllib
from rest_api import wiki_parser

from conf import *

def greq_parse(urls, logger):
    '''
    Recieves list of urls and scrape data
    :return: dataframe witn data
    '''
    reqs = [grequests.get(u) for u in urls]
    resp = grequests.map(reqs, size=STEP)

    df = pd.DataFrame(columns=COLUMNS)
    for i, r in enumerate(resp):
        if r.status_code != 200:
            logger.warning("Can't get link: " + r.request.url + " Error code: " + str(r.status_code))
            continue

        soup = BeautifulSoup(r.text, 'html.parser')

        logger.info(f'Scraping {i+1} of {len(urls)} pages')

        for each in soup.find_all(class_="result"):
            try:
                title = each.find(class_='jobtitle').text.replace('\n', '')
            except:
                title = 'None'

            try:
                location = each.find('span', {'class': "location"}).text.replace('\n', '')
            except:
                location = 'None'

            try:
                company = each.find(class_='company').text.replace('\n', '')
            except:
                company = 'None'

            #TODO put company_info into database
            if company != 'None':
                company_summary = wiki_parser(company, logger)
            else:
                company_summary = 'No summary'

            try:
                salary = each.find('span', {'class': 'no-wrap'}).text.replace('\n', '')
            except:
                salary = 'None'

            try:
                synopsis = each.find('span', {'class': 'summary'}).text.replace('\n', '')
            except:
                synopsis = 'None'

            try:
                link = each.find('a', attrs={'class': 'turnstileLink'})
                url_indeed = ROOT_URL + link.attrs['href']
            except:
                url_indeed = 'None'

            job_descriptoin, url_publisher, publish_date = parse_job_description_page(url_indeed)

            values = (title, location, company, salary, synopsis, job_descriptoin, url_indeed, url_publisher, publish_date, company_summary)
            logger.info(f'Job position {title} in company {company} downloaded with {values.count("None")} missed values')

            df = df.append({k: v for k, v in zip(COLUMNS, values)}, ignore_index=True)

    return df


def parse_job_description_page(url_indeed):
    """
    on job description page we can get additional information:
        - full job description
        - url of a publisher
        - job position publishing date (relative to current day, e.g. "3 days ago")
    :param url_indeed:
    :return:
    """

    html = requests.get(url_indeed)
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")

    try:
        job_descriptoin = soup.find(name="div", attrs={"id": "jobDescriptionText"}).text
    except:
        job_descriptoin = 'None'

    try:
        starturl = soup.find("a", string="original job").attrs['href']
        req = urllib.request.Request(starturl, None, HEADERS)
        res = urllib.request.urlopen(req)
        publisher_url = res.geturl()
    except:
        publisher_url = 'None'

    try:
        publish_date = soup.find('div', attrs={"class": "jobsearch-JobMetadataFooter"}).text
        publish_date = publish_date.split(" - ")[1]

    except:
        publish_date = 'None'

    return job_descriptoin, publisher_url, publish_date