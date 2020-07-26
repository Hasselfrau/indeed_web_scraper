import wikipedia
import urllib
import json


def wiki_parser(company, logger):
    '''

    :param company:
    :param logger:
    :return:
    '''
    try:
        w = wikipedia.WikipediaPage(company)
    except Exception as e:
        logger.warning(f"Can't find page of {company} on wikipedia")
        return 'No summary'
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{w.url.split('/')[-1]}"
    f = urllib.request.urlopen(url)
    html = f.read().decode('utf-8')
    js = json.loads(html)
    return js['extract']
