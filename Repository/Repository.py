import inspect
import json
import time

import requests
from bs4 import BeautifulSoup
from Repository import Settings

PageLimit = "[程式]已經達到上限(%d/%d)"
FailGet = "[程式]無法取得列表"
InSearch = "[程式]正在搜尋中...(%d/%d)"
RetrySearch = "[程式]無法處理搜尋回應，重試中。(%d)"

class Repository():

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def findUrl(self, url):
        try:
            response = requests.get(url=url, headers=self.headers, timeout=30)
            # beautiful Soup
            soup = BeautifulSoup(response.text, "lxml")
            elements = soup.select("dl>dd>a[href]")
            for e in elements:
                href = e['href']
                if 'live.staticflickr.com' in href:
                    return href
            return None
        except:
            return None

    def search(self, searchText, page=1, Retry=5, **kwargs):
        response = self._search(text=searchText, page=page, **kwargs)
        if response and Settings.photoPrefix in response:
            details = response[Settings.photoPrefix]
            if 'pages' in details:
                if page > details['pages']:
                    print(PageLimit % (page, details['pages']))
                    return None
                else:
                    print(InSearch % (page, details['pages']))
                    return details['photo']
            else:
                print(FailGet)
                return None
        elif Retry > 0:
            print(RetrySearch % (Retry))
            time.sleep(Settings.sleep_time)
            Retry -= 1
            self.search(searchText, page, Retry)

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
        try:
            response = requests.get(url=Settings.baseApiUrl, params=params, headers=self.headers, timeout=30)
            return json.loads(response.text)
        except:
            return None
