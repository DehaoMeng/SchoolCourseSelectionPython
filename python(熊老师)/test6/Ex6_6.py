#Ex6_6.py
import jieba
import wordcloud
from scipy.misc import imread
import matplotlib.pyplot as plt

mask = imread("fivestart.png")
excludes = { }
f = open("新时代中国特色社会主义.txt", "r", encoding="utf-8")
t = f.read()
f.close()
ls = jieba.lcut(t)
txt = " ".join(ls)
w = wordcloud.WordCloud(\
    width = 1000, height = 700,\
    background_color = "white",
    font_path = "msyh.ttc", mask = mask
    )
bmp = w.generate(txt)

plt.imshow(bmp)
plt.axis('off')
plt.show()


