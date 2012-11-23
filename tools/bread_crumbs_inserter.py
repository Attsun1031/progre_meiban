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
    # バンドファイルの場合
    if file.split('.')[-1] == shtml_ext:
        # 読み込み
        try:
            fullPath = '/'.join([searchPath, file])
            rf = codecs.open(fullPath, mode='r', encoding=enc)
            lines = rf.readlines()

        except:
            print sys.exc_info()

        finally:
            rf.close()

        # 書き込み
        try:
            wf = codecs.open(fullPath, mode='w', encoding=enc)

            for line in lines:
                wf.write(line)
                if line.find('<div id="main">') >= 0:
                    wf.write(u'\t\t\t<!--#include virtual="/common/bread_crumbs/' + unicode(os.path.splitext(file)[0], enc) + u'.html"-->\n')

        except:
            print sys.exc_info()

        finally:
            wf.close()

    # アルバムディレクトリの場合
    else:
        for album_file in os.listdir("/".join([searchPath, file])):
            # 読み込み
            try:
                fullPath = '/'.join([searchPath, file, album_file])
                rf = codecs.open(fullPath, mode='r', encoding=enc)
                lines = rf.readlines()

            except:
                print sys.exc_info()

            finally:
                rf.close()

            # 書き込み
            try:
                wf = codecs.open(fullPath, mode='w', encoding=enc)

                for line in lines:
                    wf.write(line)
                    if line.find('<div id="main">') >= 0:
                        wf.write(u'\t\t\t<!--#include virtual="/common/bread_crumbs/' + unicode("/".join([baseDir, os.path.splitext(album_file)[0]]), enc) + u'.html"-->\n')

            except:
                print sys.exc_info()

            finally:
                wf.close()
