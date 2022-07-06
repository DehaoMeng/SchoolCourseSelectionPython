# -*- coding: utf-8 -*-
"""
Created on Fri Nov 23 10:44:47 2018

@author: fengl
"""
#Ex7_5.py
import urllib.request
import re

def getHtml(url):
    html=urllib.request.urlopen(url).read()
    html= html.decode('utf-8')
    return html

def getImg(html):
    #构建正则表达式，从页面代码里提取出图片url地址。
    img_re=re.compile(r'(?<=src=")\S+?jpg')
    print("the type of html is :",type(html))
    print(html)
    img_list=img_re.findall(html)
    return img_list

def getUrl(source):
    if source.startswith("//"):
        url = "http:"+source
    else:
        url=source
    
    return url
        
html=getHtml('http://www.ifeng.com')
img_list = getImg(html)
print("正在下载图片......")

for i in range(len(img_list)):
    print(img_list[i])
    urllib.request.urlretrieve(getUrl(img_list[i]),'.\img\%s.jpg' % i)
    
print("完成图片下载......")
