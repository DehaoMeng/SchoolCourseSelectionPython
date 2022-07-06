# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 10:52:24 2018

@author: fengl
"""
#Ex7_4.py
import urllib.request
import re

def getHtml(url):
    html=urllib.request.urlopen(url).read()
    html= html.decode('utf-8')
    return html

def getImg(html):
    #构建正则表达式，从页面代码里提取出图片url地址。
    img_re=re.compile(r'(?<=data-src=")\S+?jpg')
    print("the html is :",html)
    img_list=img_re.findall(html)
    return img_list

html=getHtml('http://www.sina.com.cn')
img_list = getImg(html)
print(img_list)