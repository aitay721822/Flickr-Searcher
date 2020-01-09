import Common.Data
from ImageDownloader.Downloader import Downloader
from Repository import Settings
from Repository.Repository import Repository

if __name__ == '__main__':
    repo = Repository()
    query = input("請輸入想要尋找的東西: ")
    page = int(input("請輸入想要開始的頁數: "))
    maxPage = int(input("請輸入想要下載的頁數(每頁%d張): " % (Settings.defaultPerPage)))
    resolution = int(input("請輸入想要下載的清晰度(0:壓縮圖|1:原圖): "))

    targetPage = maxPage + page
    downloaded = 0
    response = repo.search(query, page)
    while response and page < targetPage:
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
                image = repo.findUrl(url) if resolution is 1 else None
                if image:
                    queue.append(image)
                    print("[程式] %s 已加入佇列" % (image))
                else:
                    for res in Settings.resolution:
                        if res in r:
                            queue.append(r[res])
                            print("[程式] %s 已加入佇列" % (r[res]))
                            break
            Handler = Downloader(queue, Common.Data.downloadDir, str(query))
            downloaded += Handler.download()
            print("[程式] 第 %d 頁共下載了 (%d/%d)" % (page,downloaded,maxPage*Settings.defaultPerPage))
        except Exception as e:
            print("[程式] 第 %d 頁下載失敗，錯誤訊息為：%s" % (page,str(e)))
        finally:
            page += 1
            response = repo.search(query, page)