#!/usr/bin/env python
# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
from BeautifulSoup import Tag
from BeautifulSoup import NavigableString
import os


PARENT_DIR = '/Users/atsumitatsuya/src/progre_meiban/'
FORMAT = '/'.join([PARENT_DIR, 'tools/sitemap_orig.shtml'])
HEADER = '/'.join([PARENT_DIR, 'common/header.shtml'])
SHTML_EXT = '.shtml'
formatSoup = BeautifulSoup(open(FORMAT))

# 総作品数
contentCount = 0

# 起点タグ
mainDivTag = formatSoup.find('div', {'id' : 'main-content'})

# ディレクトリをulタグに変換する
def generateUlTag(path, file, ulClass):
    # バンド名タグを生成
    fileSoup = BeautifulSoup(open('/'.join([PARENT_DIR, path, file])))
    text = fileSoup.find('h1').renderContents()
    ulTag = Tag(formatSoup, 'ul', attrs={'class' : ulClass})
    liTag = Tag(formatSoup, 'li')
    link = '/'.join([path, file])
    aTag = Tag(formatSoup, 'a', attrs={'href' : link})
    aTag.append(NavigableString(text))
    liTag.append(aTag)
    ulTag.append(liTag)

    return ulTag

# contentDivタグを生成
def generateContentDivTag(baseDir, h3text):
    import __main__

    contentDivTag = Tag(formatSoup, 'div', attrs={'class' : 'content band-content'})
    # 表題埋め込み
    h3tag = Tag(formatSoup, 'h3')
    h3tag.append(NavigableString(h3text))
    contentDivTag.append(h3tag)


    # HTML生成
    for file in os.listdir(PARENT_DIR + baseDir):
        if file.endswith(SHTML_EXT):
            # バンド名ulタグを生成
            progreUlTag = generateUlTag('/' + baseDir, file, 'column')
            albumLiTag = Tag(formatSoup, 'li')
            progreUlTag.append(albumLiTag)

            # 作品名ulタグを生成
            fileSoup = BeautifulSoup(open('/'.join([PARENT_DIR, '/' + baseDir, file])))
            albumList = []
            for albumClassTag in fileSoup.findAll('a', {'class' : 'album-name'}):
                albumList.append(albumClassTag['href'].split('/')[-1])
                __main__.contentCount += 1

            albumDir = '/'.join([baseDir, file.split('.')[0]])
            for album in albumList:
                albumUlTag = generateUlTag('/' + albumDir, album, 'child-column')
                albumLiTag.append(albumUlTag)
            contentDivTag.append(progreUlTag)

    return contentDivTag

targetTupleList = [('progressive_rock', 'プログレッシブ・ロック'), ('jazz', 'ジャズ・フュージョン'), ('other_rock', 'HR/HMなどのロック'), ('other_music', '日本のポップス、フォーク'), ('big_band', '吹奏楽、ビッグバンド')]

for t in targetTupleList:
    contentDivTag = generateContentDivTag(t[0], t[1])
    mainDivTag.append(contentDivTag)

# 結果ファイルを作成し、終了
resultFile = open('/'.join([PARENT_DIR, 'sub_contents', 'sitemap.shtml']), 'w')
#resultFile.write(formatSoup.prettify().encode('utf-8'))
resultFile.write(formatSoup.prettify())
resultFile.close()


# 共通ヘッダーファイルに総作品数を表示
headerSoup = BeautifulSoup(open(HEADER))
countTag = headerSoup.find('div', {'class' : 'contents-count'})
countTag.contents[0].replaceWith(NavigableString(u'総作品数: %d' % contentCount))

resultFile = open('/'.join([PARENT_DIR, 'common', 'header.shtml']), 'w')
resultFile.write(headerSoup.prettify())
resultFile.close()
