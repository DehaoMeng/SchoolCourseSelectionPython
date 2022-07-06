# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 21:14:54 2018

@author: fengl
"""
#Ex7_6.py
import urllib.request
from bs4 import BeautifulSoup

html = urllib.request.urlopen("http://news.sina.com.cn").read()
bsObj = BeautifulSoup(html, "html.parser")
downloadList=bsObj.select('a')
print ('__________________')
print (downloadList)
print (len(downloadList))