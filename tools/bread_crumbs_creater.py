#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from BeautifulSoup import Tag
from BeautifulSoup import NavigableString
import copy
import sys

PARENT_DIR = '/Users/atsumitatsuya/Workspace/progre_meiban'
SITEMAP = 'sub_contents/sitemap.shtml'
SITE_DOMAIN = 'http://progre-meiban.com/'

# 処理対象のバンドディレクトリ名
TARGET_BAND = sys.argv[1]


# TOPリンクタグの生成
def createParentUlTag(targetSoup):
    parentUlTag = Tag(targetSoup, 'ul', attrs={'class' : 'xbreadcrumbs', 'id' : 'breadcrumbs'})
    topListTag = Tag(targetSoup, 'li')
    topAnchorTag = Tag(targetSoup, 'a', attrs={'href' : SITE_DOMAIN})
    topAnchorTag.append(NavigableString('TOP'))
    topListTag.append(topAnchorTag)
    parentUlTag.append(topListTag)
    return parentUlTag


sitemapSoup = BeautifulSoup(open('/'.join([PARENT_DIR, SITEMAP])))
for bandContentDivTag in sitemapSoup.findAll('div', attrs = {'class' : 'content band-content'}):
    for column in bandContentDivTag.findAll('ul', attrs = {'class' : 'column'}):

        # バンドファイルのパンくずリスト
        anchorLink = column.find('a')['href']
        fileName = anchorLink.split('/')[-1].replace('.shtml', '.html')
        # 処理対象のバンドのみ処理する。指定がない場合はすべて。
        if not TARGET_BAND or fileName[:-5] == TARGET_BAND:
            bandBreadCrumbsSoup = BeautifulSoup()
            parentUlTag = createParentUlTag(bandBreadCrumbsSoup)
            bandListTag = column.find('li')
            albumUlTag = Tag(bandBreadCrumbsSoup, 'ul')
            bandListTag.append(albumUlTag)
            for childColumn in column.findAll('ul', attrs = {'class' : 'child-column'}):
                albumUlTag.append(childColumn.find('li'))
            parentUlTag.append(bandListTag)
            # ファイル生成
            resultFile = open('/'.join([PARENT_DIR, 'common/bread_crumbs', fileName]), 'w')
            resultFile.write(parentUlTag.prettify())
            resultFile.close()
            print "write %s" % fileName

            # アルバムファイルのパンくずリスト
            for childColumn in albumUlTag.findAll('li'):
                childAnchorLink = childColumn.find('a')['href']
                albumParentUlTag = copy.deepcopy(parentUlTag)
                albumParentUlTag.append(copy.deepcopy(childColumn))
                # ファイル生成
                splitList = childAnchorLink.split('/')
                childFileName = '/'.join([splitList[-3], splitList[-1]]).replace('.shtml', '.html')
                resultFile = open('/'.join([PARENT_DIR, 'common/bread_crumbs', childFileName]), 'w')
                resultFile.write(albumParentUlTag.prettify())
                resultFile.close()
                print "write %s" % childFileName
