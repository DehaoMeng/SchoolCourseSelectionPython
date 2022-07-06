# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 21:14:54 2018

@author: fengl
"""
#Ex7_7.py
import urllib.request
from bs4 import BeautifulSoup
import re

def getHtml(url):
    html=urllib.request.urlopen(url).read()
    html= html.decode('utf-8')
    return html

html = getHtml("http://news.sina.com.cn")
bsObj = BeautifulSoup(html, "html.parser")
downloadList=bsObj.select('a')

text_re=re.compile(r'(?<=_blank">)\S+(?=</a>)')
text_list=[]
for txt in downloadList:
    html="{}".format(txt)
    text_list+=text_re.findall(html)
print(text_list)
