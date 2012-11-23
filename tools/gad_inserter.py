#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import glob
import os
import sys

enc = 'utf-8'
shtml_ext = 'shtml'

PARENT_DIR = 'C:/Users/tatsuya/development/workspace/Progressive'
baseDir = 'big_band'
searchPath = '/'.join([PARENT_DIR, baseDir])
for file in os.listdir(searchPath):
    if file.split('.')[-1] != shtml_ext:
        for album_file in os.listdir("/".join([searchPath, file])):
            # 読み込み
            try:
                fullPath = '/'.join([searchPath, file, album_file])
                rf = codecs.open(fullPath, mode='r', encoding=enc)
                lines = rf.readlines()
                print fullPath
            except:
                print sys.exc_info()

            finally:
                rf.close()

            # 書き込み
            try:
                wf = codecs.open(fullPath, mode='w', encoding=enc)

                find_amazon = False
                for line in lines:
                    wf.write(line)
                    if line.find('<div class="amazon-link">') >= 0:
                        find_amazon = True
                    elif find_amazon and line.find('</div>') >= 0:
                        find_amazon = False
                        wf.write(u'\t\t\t<!--#include virtual="/common/ads.html"-->\n')

            except:
                print sys.exc_info()

            finally:
               wf.close()
