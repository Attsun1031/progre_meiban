#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import glob
import os
import sys

enc = 'utf-8'
shtml_ext = 'shtml'

PARENT_DIR = 'C:/Users/tatsuya/development/workspace/Progressive'
baseDir = 'progressive_rock'
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

                already_inserted = False
                for line in lines:
                    if line.find(u'class="youtube-movie"') >= 0:
                        already_inserted = True
                        wf.write(line)
                    elif line.find('www.youtube.com/embed/') >= 0 and not already_inserted:
                        wf.write(u'\t\t\t<div class="youtube-movie">\n')
                        wf.write(u'\t' + line)
                        wf.write(u'\t\t\t</div>\n')
                        already_inserted = True
                    else:
                        wf.write(line)

            except:
                print sys.exc_info()

            finally:
                wf.close()
