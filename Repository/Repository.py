import inspect
import json

import requests
from bs4 import BeautifulSoup
from Repository import Settings


class Repository():

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def findUrl(self, url):
        response = requests.get(url=url,headers=self.headers)
        # beautiful Soup
        soup = BeautifulSoup(response.text, "html.parser")
        elements = soup.select("dl>dd>a[href]")
        if len(elements) != 2:
            return None
        else:
            return elements[1]['href']


    def search(self, searchText, page=1, **kwargs):
        response = self._search(text=searchText, page=page, **kwargs)
        if Settings.photoPrefix in response:
            details = response[Settings.photoPrefix]
            if 'pages' in details:
                if page > details['pages']:
                    return None
                else:
                    return details['photo']
            else:
                return None

    def _search(self,
                text,
                page,
                sort=Settings.defaultSort,
                parse_tags=Settings.defaultParseTag,
                content_type=Settings.defaultContentType,
                extras=Settings.defaultExtras,
                per_page=Settings.defaultPerPage,
                lang=Settings.defaultLang,
                view_all=Settings.defaultViewALL,
                method=Settings.SearchMethod,
                format=Settings.defaultFormat,
                hermas=Settings.defaultHerMas,
                api_key=Settings.api_key,
                hermasClient=Settings.defaultHerMasClient,
                nojsoncallback=Settings.defaultnojsonCallback):
        args = dict(inspect.getargvalues(inspect.currentframe()).locals)
        # prepare params
        params = {}
        index = 0
        for k, v in args.items():
            if index != 0:
                params[k] = v
            index += 1

        # prepare request
        response = requests.get(url=Settings.baseApiUrl,params=params,headers=self.headers)
        return json.loads(response.text)