#Ex7_2.py
import matplotlib.pyplot as plt
import numpy as np
#数据读取
datals = []
f = open("SH600000.txt")
for line in f:
    line = line.replace("\n","")
    datals.append(list(line.split("\t")))
f.close()
datals = np.array(datals)

fig = plt.figure()
#设置中文显示模式
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签  
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

for i in range(6):
    ax1 = fig.add_subplot(6,1,i+1)
    ax1.plot(list(map(eval,datals[1:,i+1])))
    ax1.set_ylabel(datals[0,i+1])

plt.show()

