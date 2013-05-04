#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from BeautifulSoup import BeautifulSoup, NavigableString

HOME_PATH = '/Users/atsumitatsuya/src/progre_meiban'
SITEMAP_PATH = os.path.join(HOME_PATH, 'sub_contents/sitemap.shtml')
INCLUDE_STRING_MARK = u'!!!include_band_intro_add_here!!!'
INCLUDE_STRING = NavigableString(u'<!--#include virtual="/common/band_intro_ads.html"-->')


class BandIntroPage(object):
    def __init__(self, path):
        self.path = path
        self.soup = BeautifulSoup(open(path))

    def save(self):
        print "write: %s" % self.path
        with open(self.path, 'w') as f:
            page_contents = self.soup.prettify().decode('utf-8').replace(INCLUDE_STRING_MARK, INCLUDE_STRING)
            f.write(page_contents.encode('utf-8'))

    def find(self, *args, **kw):
        return self.soup.find(*args, **kw)

    def findAll(self, *args, **kw):
        return self.soup.findAll(*args, **kw)

    def append(self, *args, **kw):
        return self.append(*args, **kw)


class AdInserter(object):

    def __init__(self):
        sitemap_soup = None

    def prepare(self):
        self.sitemap_soup = BeautifulSoup(open(SITEMAP_PATH))

    def main(self):
        target_pages = self.get_target_pages()
        self.insert_ad_to_pages(target_pages)
        self.save_pages(target_pages)

    def get_target_pages(self):
        target_pages = []
        for column_tag in self.sitemap_soup.findAll('ul', {'class': 'column'}):
            li_tag = column_tag.find('li')
            if li_tag is None:
                continue
            a_tag = li_tag.find('a')
            if a_tag is None:
                continue

            band_page_path = a_tag['href']
            if band_page_path.startswith('/'):
                band_page_path = band_page_path[1:]
            abs_band_page_path = os.path.join(HOME_PATH, band_page_path)
            print "target path: %s" % abs_band_page_path
            target_pages.append(BandIntroPage(abs_band_page_path))

        return target_pages

    def insert_ad_to_pages(self, target_pages):
        for page in target_pages:
            content_div = page.findAll('div', {'class': 'content'})[-1]
            content_div.append(INCLUDE_STRING_MARK)

    def save_pages(self, target_pages):
        for page in target_pages:
            page.save()

    def finalize(self):
        pass

    @classmethod
    def run(cls):
        ins = AdInserter()
        ins.prepare()
        ins.main()
        ins.finalize()


if __name__ == '__main__':
    AdInserter.run()
