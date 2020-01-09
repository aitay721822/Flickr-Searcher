import os
import sys
import time
from multiprocessing.pool import Pool
import requests

Downloaded = "[圖片] %s 下載成功"
DownloadError = '[圖片] %s 下載錯誤，已放棄下載'
DownloadErrorRetry = "[圖片] %s 下載錯誤 (%d) ，重試中(%d)"
DownloadOutTimeRetry = "[圖片] %s 下載超時，重試中(%d)"


class Downloader:

    def __init__(self, urlQueue, download_dir, dir_name):
        self.urlQueue = urlQueue
        self.download_dir = download_dir
        self.dir_name = dir_name

    def _run(self, url):
        isDownloaded = False
        try:
            storagePath = self.download_dir + "/" + self.dir_name
            if not os.path.exists(storagePath):
                os.makedirs(storagePath)
            remaining_download_tries = 10
            imgPath = storagePath + "/" + url.split("/")[-1:][0]
            while remaining_download_tries > 0 and os.path.isfile(imgPath) is False:
                try:
                    response = requests.get(url, timeout=30)
                    if response and response.status_code == 200:
                        print(Downloaded % (url))
                        with open(imgPath, 'wb') as f:
                            f.write(response.content)
                            f.flush()
                            f.close()
                        isDownloaded = True
                        break
                    else:
                        print(DownloadError % (url, response.status_code, remaining_download_tries))
                except:
                    print(DownloadOutTimeRetry % (url, remaining_download_tries))
                finally:
                    remaining_download_tries -= 1
            if remaining_download_tries <= 0:
                print(DownloadErrorRetry % url)
        finally:
            return isDownloaded

    def download(self):
        result = []
        if self.urlQueue:
            pool = Pool(processes=4)
            result = pool.map(self._run, self.urlQueue)
            pool.close()
            pool.join()
        complete = 0
        for r in result:
            if r:
                complete += 1
        return complete
