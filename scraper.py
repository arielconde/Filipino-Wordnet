import time
import os
from queue import *
import requests
import bs4
import utils
import os


"""
Set character encoding in CMD to UTF-8
This is to avoid crash and to process non ASCII characters
"""
os.system("chcp 65001")

MAX_SCRAPING_COUNT = 2000

ARTICLES_FOLDER = 'articles/'

q = Queue(maxsize=100)


def run_scraper(letter, page_no):
    seed = 'http://tagalog.pinoydictionary.com/list/' + \
        letter + '/' + str(page_no) + '/'
    print('Requesting:', seed)
    res = requests.get(seed)

    # check if the page is not available
    # the move to the next letter
    if res.status_code == 404:
        print('Page', page_no, "can't be reach for Letter: ", letter)
        letter = chr(ord(letter) + 1)
        page_no = 0
        run_scraper(letter, page_no)
    # if availabe perform scraping
    else:
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        wikiseeds = soup.select('h2.word-entry > a')
        for seed in wikiseeds:
            print(letter, page_no, 'Getting article for:', seed.getText())
            wikilink = 'https://tl.wikipedia.org/wiki/' + seed.getText()
            reswiki = requests.get(wikilink)
            wikisoup = bs4.BeautifulSoup(reswiki.text, "html.parser")
            paragraphs = wikisoup.select("p")
            text = str(paragraphs[0].getText().encode('ascii', 'ignore'))
            text = utils.clean_paren(text)
            if 'Walang teksto' in text:
                continue
            else:
                filepath = ARTICLES_FOLDER + seed.getText() + '.txt'
                f = open(filepath, 'w')
                f.write(text)
                f.close()
                print(text)
        # all of the seed in the first page is consumed
        # move to the next page
        run_scraper(letter, page_no + 1)


if __name__ == '__main__':
    letter = 'a'
    page_no = 4
    run_scraper(letter, page_no)
