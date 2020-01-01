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
    def __init__(self,urlQueue,download_dir,dir_name):
        self.urlQueue = urlQueue
        self.download_dir=download_dir
        self.dir_name = dir_name

    def _run(self,url):
        storagePath = self.download_dir + "/" + self.dir_name
        if not os.path.exists(storagePath):
            os.makedirs(storagePath)
        remaining_download_tries = 10
        while remaining_download_tries > 0:
            try:
                response = requests.get(url,timeout=30)
                if (response and response.status_code == 200):
                    print(Downloaded % (url))
                    imgPath = storagePath + "/" + url.split("/")[-1:][0]
                    with open(imgPath, 'wb') as f:
                        f.write(response.content)
                        f.flush()
                        f.close()
                    break
                else:
                    print(DownloadError % (url, response.status_code, remaining_download_tries))
            except:
                print(DownloadOutTimeRetry % (url,remaining_download_tries))
            finally:
                remaining_download_tries -= 1
        if remaining_download_tries <= 0:
            print(DownloadErrorRetry % (url))
        time.sleep(2)


    def download(self):
        if self.urlQueue:
            pool = Pool(processes=4)
            for i in self.urlQueue:
                pool.apply_async(self._run,(i,))
            pool.close()
            pool.join()
