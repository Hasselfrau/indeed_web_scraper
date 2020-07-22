import pandas as pd
from bs4 import BeautifulSoup
import requests
import urllib


def parse_job_description_page(url_indeed):
    """
    on job description page we can get additional information:
        - full job description
        - url of a publisher
        - job position publishing date (relative to current day, e.g. "3 days ago")
    :param url_indeed:
    :return:
    """

    HEADERS = {
        'User-Agent': 'My User Agent 1.0',
        'From': 'youremail@domain.com'
    }

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


def parse_list_of_jobs(input_url):
    html = requests.get(input_url)
    soup = BeautifulSoup(html.content, 'html.parser', from_encoding="utf-8")
    df = pd.DataFrame(columns=["Title", "Location", "Company", "Salary", "Synopsis", "Description",
                               "URL_indeed", "URL_publisher", "Publish_date"])

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
            url_indeed = "https://www.indeed.com" + link.attrs['href']
        except:
            url_indeed = 'None'

        job_descriptoin, url_publisher, publish_date = parse_job_description_page(url_indeed)

        df = df.append(
            {'Title': title,
             'Location': location,
             'Company': company,
             'Salary': salary,
             'Synopsis': synopsis,
             'Description': job_descriptoin,
             'URL_indeed': url_indeed,
             'URL_publisher': url_publisher,
             'Publish_date': publish_date
             }, ignore_index=True)
    return df
