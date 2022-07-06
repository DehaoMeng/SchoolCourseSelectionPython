# 调用库
import asyncio
from aiohttp import ClientSession
import urllib.request
from bs4 import BeautifulSoup
from lxml import etree
import re
import time
from wordcloud import WordCloud
import jieba
import collections
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
jieba.setLogLevel(jieba.logging.INFO)

class Get_news():
    """
     获取新闻网页内容和新闻内容并将文字保存到本地
    """
    def __init__(self):
        """ 初始化该类 """
        # 输入新闻网页
        self.html = 'https://news.sina.com.cn/china/'  # 新闻网址
        self.div_list = self.getnews_herf(self.html) # 调用函数获取新闻网页中的url的div标签。
        # 新建一个列表，存储具体的新闻url
        url_list = []
        # 循环判断列表中是否有空值
        for i in self.div_list:
            # 删除获得空值
            if i == '':
                div_list.remove(i)
        # 循环输入最新的30篇新闻url
        for div in self.div_list[0:31]:
            # xpath获得a标签中的新闻url
            url = div.xpath('./a/@href')[0]
            # 将url加入到之前创建的空列表
            url_list.append(url)
        # 任务列表对象tasks，利用循环将url_list中的每个url都进行爬取操作加入到tasks中
        tasks = [asyncio.ensure_future(self.write_news(new_url)) for new_url in url_list]
        # 获取循环事件
        loop =  asyncio.get_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(asyncio.wait(tasks))
        # 关闭打开的新闻文本文档
        self.f.close()


    def getnews_herf(self,url):
        """
         获取网页中具体新闻的div标签列表
        """
        # 获得新闻网站的响应数据
        html = urllib.request.urlopen(url).read()
        html = html.decode('utf-8')
        # 获取url的div标签
        tree = etree.HTML(html)
        div_list = tree.xpath('//div[@class="left-content-1 marBot"]/div/ul/li')
        # 返回div列表
        return div_list

    async def write_news(self,new_url):
        # 打开文件
        self.f = open('news.txt','w',encoding='utf-8')
        async with ClientSession() as session:
            # 使用异步编程访问网页
            async with session.get(new_url) as response:
                # 输出日志,保存爬取网页url和时间
                # 一次获取网页的响应,等待期间执行下一次响应(挂起操作)
                response = await response.text(encoding='utf-8')
                # bs_obj为网页信息
                bs_obj = BeautifulSoup(response, 'html.parser')
                # 获取网站内的<p>标签内容
                downloadList = bs_obj.select('p')
                # 创建一个空列表，后续存入新闻内容。
                text_list = []
                # 获取符合条件的<p>标签内容
                text_re = re.compile(r'<p ?(cms-style="font-L")?>(\s+?\S+?)</p>')
                # print(downloadList)
                for txt in downloadList:
                    # 所有的p标签内容依次匹配
                    html="{}".format(txt)
                    # 比较符合条件的p标签内容,将符合内容的加入到文本列表中
                    text_list += text_re.findall(html)
                # 挂起写入操作,减少响应时间
                await self.write_file(text_list)

    async def write_file(self,text_list):
        # 向文本文件内写入新闻信息
        for txt in text_list:
            self.f.write(txt[1])
        self.f.write('\n爬取时间：'+str((time.strftime("%Y-%m-%d %H：%M：%S", time.localtime())))+'\n')
        self.f.write('\n')

class Dispose(object):
    """
    处理数据并生成词云
    """
    def __init__(self):
        """ 初始化处理数据类 """
        with open('news.txt','r',encoding='utf-8') as f:
            data = f.read()
        self.word_counts_top100=dict(self.dispose(data))
        self.create_word_cloud()

    def dispose(self,data):
        """
         文本预处理  去除一些无用的字符   只提取出中文出来
         """
        self.new_data = re.findall('[\u4e00-\u9fa5]+', data, re.S)
        self.new_data = " ".join(self.new_data)
        # 文本分词
        self.seg_list_exact = jieba.cut(self.new_data, cut_all=True)
        self.result_list = []
        for word in self.seg_list_exact:
            # 设置停用词并去除单个词
            if len(word) > 1:
                self.result_list.append(word)

        # 筛选后统计
        word_counts = collections.Counter(self.result_list)
        # 获取前100最高频的词
        word_counts_top100 = word_counts.most_common(100)
        return word_counts_top100

    def create_word_cloud(self):
        """ 打开词云 """
        image= Image.open('ditu.png')#打开背景图
        graph = np.array(image)#读取背景图
        # 绘制词云
        my_cloud = WordCloud(
            background_color='white',  # 设置背景颜色  默认是black
            width=900, height=600,
            max_words=101,            # 词云显示的最大词语数量
            font_path='simhei.ttf',   # 设置字体  显示中文
            max_font_size=800,         # 设置字体最大值
            min_font_size=10,         # 设置子图最小值
            random_state=50,          # 设置随机生成状态，即多少种配色方案
            mask=graph                # 设置背景模板
        ).generate_from_frequencies(self.word_counts_top100)
        # 显示生成的词云图片
        plt.imshow(my_cloud, interpolation='bilinear')
        # 显示设置词云图中无坐标轴
        plt.axis('off')
        plt.show()
        my_cloud.to_file('3.png')

Get_news()
Dispose()