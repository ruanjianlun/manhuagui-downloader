import sys
import time
import random
import requests
from urllib3 import Retry
from requests.adapters import HTTPAdapter

from downloadr_session import MangaDownloaderSession

"""
该脚本下载所有章节的漫画需要指定manga_id
添加useAgent，session 避免被封
使用方式：
python ScrIpSession.py 45263
"""


def create_session():
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com'
    }
    session.headers.update(headers)
    return session


def download_all_chapters(manga_id, download_path):
    url = f"https://www.manhuagui.com/comic/{manga_id}/"
    session = create_session()

    try:
        downloader = MangaDownloaderSession(url, download_path, session=session)
    except Exception as e:
        print(f"Failed to initialize downloader: {e}")
        return

    print(f"Downloading manga: {downloader.title}")
    print(f"Author: {downloader.author}, Year: {downloader.year}, Region: {downloader.region}, Plot: {downloader.plot}")

    existing_chapters = downloader.existedChapters()

    for chapter in downloader.chapters:
        chapter_title, chapter_url, _ = chapter
        if chapter_title in existing_chapters:
            print(f"Chapter {chapter_title} already exists, skipping...")
        else:
            print(f"Downloading chapter: {chapter_title}")
            try:
                downloader.downloadChapter(chapter_url)
                print(f"Chapter {chapter_title} downloaded successfully.")
            except Exception as e:
                print(f"Failed to download chapter {chapter_title}: {e}")

            # Random delay between requests to avoid being blocked
            time.sleep(random.uniform(1, 5))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <manga_id>")
        sys.exit(1)

    manga_id = sys.argv[1]
    download_path = 'manga/'  # Specify your desired download path here
    download_all_chapters(manga_id, download_path)
