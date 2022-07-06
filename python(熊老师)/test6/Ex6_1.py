# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 20:23:16 2018

@author: fengl
"""
import scipy.io.wavfile as wavf
import matplotlib.pyplot as plt
import numpy as np

#读wav文件，并对声音数据转换为-1~1之间的实数，返回帧率和声音振幅数据（单声道）
def readWav(wavefn):
    (r,s) = wavf.read(wavefn)
    if s.dtype == np.int16:
        s = s/32768.0
    elif s.dtype == np.int32:
        s = s/2147483648.0
    elif s.dtype == np.uint8:
        s = s/256.0 
        
    if (len(s.shape)>1):
        s = s[:,0]
    else:
        s = s
    
    return (r,s)

#声音信息分帧函数
def enframe(signal, nw):
 
    signal_length=len(signal) #信号总长度
    if signal_length<=nw: #若信号长度小于一个帧的长度，则帧数定义为1
        nf=1
    else: #否则，计算帧的总长度
        nf=int(np.ceil((1.0*signal_length)/nw))

    pad_length=int(nf*nw) #所有帧加起来总的铺平后的长度
    zeros=np.zeros((pad_length-signal_length)) #不够的长度使用0填补
    pad_signal=np.concatenate((signal,zeros)) #填补后的信号记为pad_signal
    frames=pad_signal.reshape(nf,nw) #得到帧信号
    return frames   #返回帧信号矩阵

#求帧的一般过零率
def RMS(x):
  return sum(x**2)/len(x);

def fRMS(x):   #x为声音数据 **%
    # 循环计算各帧过零率 ****
    dtm = np.zeros((x.shape[0]))
    for i in range(0,x.shape[0]-1): 
        dtm[i]=RMS(x[i,:]);       

    return (dtm-dtm.min())/(dtm.max()-dtm.min())

#求帧的一般过零率
def ZCR(x):
  signs = np.sign(x)
  signs[signs == 0] = -1

  return len(np.where(np.diff(signs))[0])/len(x)

#计算声音数据的各帧一般过零率
def fZCR(x):   #x为声音数据 
    # 循环计算各帧过零率 ****
    dtm = np.zeros((x.shape[0]))
    for i in range(0,x.shape[0]-1): 
        dtm[i]=ZCR(x[i,:]);       

    return (dtm-dtm.min())/(dtm.max()-dtm.min())


(rate,wav) = readWav("explosion_1.wav")

fwav = enframe(wav,256)
m_zcr = fZCR(fwav)
m_rms = fRMS(fwav)

fig = plt.figure()
ax1 = fig.add_subplot(311)

ax1.plot(wav,color=(0.1,0.1,1.0),linewidth=0.5)
ax1.set_xlabel("time", color="black")
ax1.set_ylabel("wave")

ax1 = fig.add_subplot(312)
ax1.plot(m_zcr, 'r',linewidth=1)
ax1.set_xlabel("frame", color="black")
ax1.set_ylabel("ZCR")

ax1 = fig.add_subplot(313)
ax1.plot(m_rms, 'b',linewidth=1)
ax1.set_xlabel("frame", color="black")
ax1.set_ylabel("RMS")

plt.show()
