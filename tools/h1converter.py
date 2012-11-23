#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from BeautifulSoup import Tag

import codecs
import glob
import os
import sys

enc = 'utf-8'
shtml_ext = 'shtml'

PARENT_DIR = 'C:/Users/tatsuya/development/workspace/Progressive'
baseDir = 'sub_contents'
searchPath = '/'.join([PARENT_DIR, baseDir])

def convert(dir, file):
    if dir:
        fullPath = '/'.join([searchPath, dir, file])
    else:
        fullPath = '/'.join([searchPath, file])
    soup = BeautifulSoup(open(fullPath).read())
    
    pageTitleDiv = soup.find('div',{'id':'page-title'})
    tag = Tag(soup, 'h1')
    tag.insert(0, pageTitleDiv.renderContents())
    pageTitleDiv.replaceWith(tag)

    f = open(fullPath, 'w')
    f.write(soup.prettify())
    f.close()

if __name__ == '__main__':
    for file in os.listdir(searchPath):
        if file.split('.')[-1] != shtml_ext:
            for album_file in os.listdir("/".join([searchPath, file])):
                print album_file
                try:
                    convert(file, album_file)
                except Exception:
                    print "%s is failed" % album_file
        else:
            print file
            try:
                convert(None, file)
            except Exception:
                print "%s is failed" % file
