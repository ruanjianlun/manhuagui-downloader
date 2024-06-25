import sys
from downloader import MangaDownloader

"""
该脚本下载所有章节的漫画需要指定manga_id
"""
def download_all_chapters(manga_id, download_path):
    url = f"https://www.manhuagui.com/comic/{manga_id}/"
    try:
        downloader = MangaDownloader(url, download_path)
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


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <manga_id>")
        sys.exit(1)

    manga_id = sys.argv[1]
    download_path = 'manga/'  # Specify your desired download path here
    download_all_chapters(manga_id, download_path)
