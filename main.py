import Common.Data
from ImageDownloader.Downloader import Downloader
from Repository import Settings
from Repository.Repository import Repository

if __name__ == '__main__':
    repo = Repository()
    query = input("請輸入想要尋找的東西: ")
    page = int(input("請輸入想要開始的頁數: "))
    maxDownload = int(input("請輸入想要下載的數量: "))
    downloaded = 0
    response = repo.search(query, page)
    while (response and downloaded < maxDownload):
        try:
            queue = []
            for r in response:
                if downloaded >= maxDownload:
                    break
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
                    downloaded += 1
                    print("[程式] %s 已加入佇列" % (image))
                else:
                    for res in Settings.resolution:
                        if res in r:
                            queue.append(r[res])
                            downloaded += 1
                            print("[程式] %s 已加入佇列" % (r[res]))
                            break

            Handler = Downloader(queue, Common.Data.downloadDir, str(query))
            Handler.download()
        except:
            print("[程式] 第 %d 頁下載失敗" % (page))
        finally:
            page += 1
            response = repo.search(query, page)
