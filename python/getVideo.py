#!/usr/bin/env python
#coding: utf-8
import os
import sys
import re
import urllib
import requests
from bs4 import BeautifulSoup as bs

save_path = os.environ["HOME"] + "/Downloads/"
input_url = raw_input("Please input a valid netease open course link: ")


if not input_url:
    print "Please input a valid url!"
    sys.exit(1)

def getPlaylistName(url):
    '''
    return the playlist name for mkdir for a playlist
    '''
    if url.endswith("html"):
        return url.split("/")[-1].split(".")[0]
    else:
        return url.split("/")[-2]

def getUrlList(url):
    resp = requests.get(url)
    soup = bs(resp.text, "lxml")
    #获取包含URL列表的JavaScript脚本代码(unicode)
    table = soup.find_all(class_="m-clist", style="")
    print table
    #pattern = re.compile(r"href:'http://open.163.com/.+?html'")
    #urlist = pattern.findall(script)
    #if urlist:
    #    print urlist
    #    return urlist
    #else:
    #    print "Url list is none!"

def getVideo(url):
    resp = requests.get(url)
    #it is single video if the string "m3u8" in the response text else playlist.
    if u"m3u8" in resp.text:
        url_pattern = re.compile(r"http://mov.bn.netease.com.+?m3u8")
        title_pattern = re.compile(r"title :.+?,")
        url_match = url_pattern.search(resp.text)
        title_match = title_pattern.search(resp.text)
        if url_match and title_match:
            title = title_match.group().split("'")[1].encode("utf-8") + ".mp4"
            mp4url = url_match.group().replace("m3u8", "mp4")
            ret = urllib.urlretrieve(mp4url, save_path + title)
            print "**" * 20 + "Tips" + "**" * 20
            print "{filename} has been saved at {location}".format(filename=title, location=save_path)
    else:
        new_path = save_path + getPlaylistName(url)
        if not os.path.exists(new_path):
            os.mkdir(new_path)
        urlist = getUrlList(url)
        for u in urlist:
            getVideo(u)







if __name__ == "__main__":
    getUrlList(input_url)
    #getVideo(input_url)
