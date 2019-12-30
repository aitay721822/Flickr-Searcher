import Common.Data
from ImageDownloader.Downloader import Downloader
from Repository import Settings
from Repository.Repository import Repository

if __name__ == '__main__':
    repo = Repository()
    query = input("請輸入想要尋找的東西: ")
    page = 1
    response = repo.search(query, page)
    while (response):
        try:
            queue = []
            for r in response:
                if 'id' not in r and 'owner' not in r:
                    continue
                url = "%s/%s/%s/%s/%s" % (
                    Settings.baseUrl,
                    Settings.photoPrefix,
                    r['owner'],
                    r['id'],
                    Settings.sizePrefix
                )
                image = repo.findUrl(url)
                if image:
                    queue.append(image)
                    print("[程式] %s 已加入佇列" % (image))
                else:
                    for res in Settings.resolution:
                        if res in r:
                            queue.append(r[res])
                            break
                    print("[程式] %s 已加入佇列" % (r[res]))

            Handler = Downloader(queue, Common.Data.downloadDir, str(query))
            Handler.download()
        except:
            print("[程式] 第 %d 頁下載失敗" % (page))
            pass
        finally:
            page += 1
            response = repo.search(query, page)
