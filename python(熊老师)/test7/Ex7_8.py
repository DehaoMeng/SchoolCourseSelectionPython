# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 21:14:54 2018

@author: fengl
"""
#Ex7_8.py
import urllib.request
from bs4 import BeautifulSoup
import re

def getHtml(url):
    html=urllib.request.urlopen(url).read()
    html= html.decode('utf-8')
    return html

html = getHtml("https://news.sina.com.cn/c/xl/2018-12-01/doc-ihmutuec5171858.shtml")
bsObj = BeautifulSoup(html, "html.parser")
downloadList=bsObj.select('p')

text_re=re.compile(r'<p>(\s+?\S+?)</p>')
text_list=[]
for txt in downloadList:
    html="{}".format(txt)
    text_list+=text_re.findall(html)
print(text_list)
