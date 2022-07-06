# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 10:31:36 2018

@author: fengl
"""
#Ex7_3.py
import urllib.request

def getHtml(url):
    html=urllib.request.urlopen(url).read()
    html= html.decode('utf-8')
    return html

html=getHtml('http://www.baidu.com')
print(html)
