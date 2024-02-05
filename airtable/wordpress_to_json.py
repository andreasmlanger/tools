"""
Downloads text and images from a WordPress site
"""

from dotenv import load_dotenv
import requests
import urllib.request
from bs4 import BeautifulSoup
from datetime import datetime
import json
import os
import shutil
import sys
import threading


IMAGE_FOLDER = 'images'
ZIP = True
WIDTH = 300  # width of downloaded images


def download_image(url, file_name):
    url = get_fixed_image_width(url)
    urllib.request.urlretrieve(url, os.path.join(os.getcwd() + f'\\{IMAGE_FOLDER}', file_name))


def get_fixed_image_width(url, width=WIDTH):
    return url.split('?')[0] + f'?w={width}'


class Wordpress:
    @staticmethod
    def downloader(site, download_images):
        threads = []  # store image download threads
        data = []
        fw = open(site + '.txt', 'w')
        page = 1
        while True:
            url = f'https://{site}.wordpress.com/page/{page}'
            try:
                source = requests.get(url).text
            except requests.exceptions.ConnectionError:
                sys.exit('No Internet connection!')
            soup = BeautifulSoup(source, 'html.parser')
            if 'Seite nicht gefunden' in soup.title.text:
                break
            articles = soup.findAll('article')
            print(f'Downloading page #{page}')
            for article in articles:
                title = article.find('h1', attrs={'class': 'entry-title'}).string
                date_string = article.find('time', attrs={'class': 'entry-date'}).string
                date_obj = datetime.strptime(date_string, '%d/%m/%Y')
                txt_date = date_obj.strftime('%Y-%m-%d')
                img_date = date_obj.strftime('%y%m%d')
                tags = [a.string for a in article.find('span', attrs={'class': 'tags-links'}).findAll('a')]
                fw.write(f'{txt_date} | {title} | {", ".join(tags)}\n')
                idx = 1
                content = ''
                for c in article.findAll(['p', 'img']):
                    if c.get('src'):
                        img_file_name = f'{img_date}_{"%02d" % idx}.jpg'
                        idx += 1
                        thread = threading.Thread(target=download_image, args=(c.get('src'), img_file_name))
                        threads.append(thread)
                        content += '{' + img_file_name + '}\n'
                    elif c.getText() != '' and c.getText() != '\u00a0':
                        content += f'{c.getText()}\n'
                fw.write(f'{content}---\n')

                data.append({'Title': title, 'Date': txt_date, 'Tags': tags, 'Content': content.rstrip('\n')})
            page += 1
        fw.close()
        with open('data.json', 'w') as fp:
            json.dump(data, fp)
        if download_images == 'y':
            if not os.path.exists(os.getcwd() + f'\\{IMAGE_FOLDER}'):
                os.makedirs(os.getcwd() + f'\\{IMAGE_FOLDER}')
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join()  # wait for all threads to end
            if ZIP:
                shutil.make_archive(site, 'zip', os.getcwd() + f'\\{IMAGE_FOLDER}')
                shutil.rmtree(os.getcwd() + f'\\{IMAGE_FOLDER}')
        print('\033[36m' + 'Download complete!')


def main():
    load_dotenv()
    default = os.getenv('DEFAULT_WORDPRESS_SITE')
    site = input('\033[94m' + 'Which Wordpress site would you like to download?'
                              ' (default: \033[92m' + default + '\033[94m)\n') or default
    download_images = input('\033[94m' + 'Also download images? (y/n) (default: \033[92m' + 'n' + '\033[94m)\n') or 'n'
    Wordpress.downloader(site, download_images)


if __name__ == main():
    main()
