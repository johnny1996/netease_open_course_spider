#!/usr/bin/env python
#coding: utf-8
#
#1. 这是一个小脚本程序，可以批量下载网易公开课的一门课程，也可以单独下载课程中的某一个视频。
#2. 用法简单，python getVideo.py 即可~
#3. 下载位置默认为当前位置
import os
import sys
import re
import urllib
import requests
from bs4 import BeautifulSoup as bs

savePath = os.path.dirname(os.path.abspath(__file__))
#inputUrl = raw_input("请输入网易公开课的视频链接: ")
inputUrl = "http://open.163.com/movie/2011/5/K/3/M807BPK1K_M80A0VVK3.html"

def getUrlList(url):
    resp = requests.get(url)
    soup = bs(resp.text, "lxml")
    #获取包含URL列表的JavaScript脚本代码(unicode)
    script = soup.find_all("script")[-2].get_text()
    pattern = re.compile(r"href:'http://open.163.com/.+?html'")
    match = pattern.findall(script)
    if match:
        return match

def getVideo(url):
    resp = requests.get(url)
    print type(resp.text)
    #通过判断网页代码中是否含有'm3u8'字符来确定输入的链接是单个视频或视频集合
    if u"m3u8" in resp.text:
        url_pattern = re.compile(r"http://mov.bn.netease.com.+?m3u8")
        title_pattern = re.compile(r"title :.+?,")
        url_match = url_pattern.search(resp.text)
        title_match = title_pattern.search(resp.text)
        if url_match and title_match:
            title = title_match.group().split("'")[1].encode("utf-8") + ".mp4"
            mp4url = url_match.group().replace("m3u8", "mp4")
            ret = urllib.urlretrieve(mp4url, title)






if __name__ == "__main__":
    #print getUrlList(inputUrl)
    getVideo(inputUrl)
