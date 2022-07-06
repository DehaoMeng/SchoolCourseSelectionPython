#Ex6_3.py
from PIL import Image
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import numpy as np
jieba.setLogLevel(jieba.logging.INFO)
file = [("三国演义","fivestart.png"),("我与地坛","chinamap.jpg"),("红楼梦","qq.png")]
def CreatWordcloud(filename,picturename):
    txt = open(filename+".txt", "r", encoding='utf-8').read()
    words  = jieba.lcut(txt)
    counts = {}
    for word in words:
        if len(word) == 1:
            continue
        else:
            counts[word] = counts.get(word,0) + 1
    items = list(counts.items())
    items.sort(key=lambda x:x[1], reverse=True)
    allcount = 0
    ls =[]
    for word, count in items:
        if(allcount <= (len(words)*0.8)):
            ls.append((word,count))
            allcount += count
    print("{}中约有{}个单词，其中大约{}个词出现的频率占总词的的80%".format(filename,len(words),len(ls)))
    image= Image.open(picturename)#打开背景图
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
        ).generate_from_frequencies(dict(items))
        # 显示生成的词云图片
    plt.imshow(my_cloud, interpolation='bilinear')
    # 显示设置词云图中无坐标轴
    plt.axis('off')
    plt.show()

for filename,picturename in file:
    CreatWordcloud(filename,picturename)