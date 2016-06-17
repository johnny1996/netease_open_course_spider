#!/usr/bin/env python
#coding: utf-8
#通过判断网页中是否含有"m3u8"字符来判断请求的是单集还是系列视频
import os
import sys
import re
import json
import urllib
import requests
from bs4 import BeautifulSoup as bs

save_path = os.environ["HOME"] + "/Downloads/"

headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "__gads=ID=133bc7c80f9a6bc9:T=1458705921:S=ALNI_MYAXRgD8ZEvi_cYophLSvFwop6WcA; _ntes_nnid=3c129ae77f08e95bf9f98b9f05f22f6e,1458705924051; _ntes_nuid=3c129ae77f08e95bf9f98b9f05f22f6e; vjuids=d7969e427.153a1a60067.0.aa1fa4f008067; usertrack=c+5+hVb3pVeQ5WPRFQbYAg==; NTES_CMT_USER_INFO=46864393%7Cwufeiquncn%7Chttp%3A%2F%2Fmimg.126.net%2Fp%2Fbutter%2F1008031648%2Fimg%2Fface_big.gif%7Cfalse%7Cd3VmZWlxdW5fY25AMTI2LmNvbQ%3D%3D; _ga=GA1.2.1480578998.1459070296; P_INFO=wufeiqun_cn@126.com|1465043876|0|open|00&15|bej&1464697983&open#bej&null#10#0#0|153212&0||wufeiqun_cn@126.com; vjlast=1458705924.1465125553.11; ne_analysis_trace_id=1466059460853; __oc_uuid=ef70f4d0-2608-11e6-9395-0fd6663dd3a6; __utma=187553192.1480578998.1459070296.1466066343.1466070700.12; __utmc=187553192; __utmz=187553192.1466070700.12.6.utmcsr=open.163.com|utmccn=(referral)|utmcmd=referral|utmcct=/ocw/; pgr_n_f_l_n3=05d2663574d4f2ab14660708923192170; JSESSIONID-WNC-98XSE=5f1c5bd67836d4cf24551d09600f582d382b7c5e59db9825130568a306bd50a5d7aea0bb98b7113800f8a0bbea48912e9046249bdee6f3faac2431c8573cd9c7e9a2dd654056a14ca7d5e256b6c87da7cc0c548e51113aeae1af526590f1fade49cca21932de6fa4ac84fde2e9f38e513f31926ffc3e1c032c19b47a01558553fb1c8a95%3A1466078033423; _lkiox7665q_=26; vinfo_n_f_l_n3=05d2663574d4f2ab.1.20.1458705924225.1466071251627.1466075047005; s_n_f_l_n3=05d2663574d4f2ab1466073202009",
        "DNT": 1,
        "Host": "open.163.com",
        "Pragma": "no-cache",
        "Referer": "http://open.163.com/",
        "Upgrade-Insecure-Requests": 1,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36"
        }


class Downloader(object):
    def __init__(self, url):
        self.url = url
        resp = requests.get(self.url, headers=headers)
        self.soup = bs(resp.text, "lxml")
        if "m3u8" in resp.text:
            self.single = True
        else:
            self.single = False

    def mkPlaylistDir(self):
        '''
        获得系列课程的英文名称并创建本地目录
        '''
        if not self.single:
            if self.url.endswith("html"):
                dirname = self.url.split("/")[-1].split(".")[0]
            else:
                dirname = self.url.split("/")[-2]
            self.dirname = dirname
            try:
                os.mkdir(save_path+dirname)
                print "**" * 20 + "{dirname}已经创建".format(dirname=dirname) + "**" * 20
            except:
                print "目录已经存在!"

    def getUrlList(self):
        '''
        获取系列课程中每一集的名称和视频链接
        return:
        [{url:xxx, title:xxx}, {url:xxx, title:xxx}, ...]
        '''
        self.urlist = []
        if self.single:
            link = {}
            link["title"] = self.soup.find(class_="sname").get_text()
            link["url"]   = self.url
            self.urlist.append(link)
        else:
            table = self.soup.find_all(class_="m-clist", attrs={"style": ""})
            tbody = table[0].find_all(class_="u-ctitle")
            for tr in tbody:
                link = {}
                link["title"] = tr.get_text().replace("\n", "").replace(" ", "")
                link["url"]   = tr.a.get("href")
                self.urlist.append(link)

    def getVideo(self):
        for li in self.urlist:
            resp = requests.get(li["url"], headers=headers)
            title = li["title"] + ".mp4"
            url_pattern = re.compile(r"http://mov.bn.netease.com.+?m3u8")
            url_match = url_pattern.search(resp.text)
            if url_match:
                mp4url = url_match.group().replace("m3u8", "mp4")
                print u"*************************************即将下载 {filename}***********************************".format(filename=title)
                if self.single:
                    ret = urllib.urlretrieve(mp4url, save_path + title)
                else:
                    ret = urllib.urlretrieve(mp4url, save_path+self.dirname+"/"+title)
                print u"************************************{filename} 下载完成!************************************".format(filename=title)
            else:
                print "未匹配到任何视频链接地址!"


if __name__ == "__main__":
    input_url = raw_input("请输入一个网易公开课的链接(单集链接或者课程链接): ")

    if not input_url:
        print "请输入一个有效的链接!"
        sys.exit(1)

    d = Downloader(input_url)
    d.mkPlaylistDir()
    d.getUrlList()
    d.getVideo()
