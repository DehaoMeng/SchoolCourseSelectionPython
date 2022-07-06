import scipy.io.wavfile as wavf
import matplotlib.pyplot as plt
import numpy as np
# 文件名称
file = ["explosion_1","gun_1","noise_1","screaming_1"]

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

zcrs_min = []
zcrs_max= []
zcrs_ave = []
zcrs_std = []
rmss_min = []
rmss_max= []
rmss_ave = []
rmss_std = []
# 循环保存每个文件的最大值 最小值 平均值 标准差
for filename in file:
    (rate,wav) = readWav(filename+".wav")
    fwav = enframe(wav,256)
    m_zcr = fZCR(fwav)
    zcrs_min.append(np.min(m_zcr))
    zcrs_max.append(np.max(m_zcr))
    zcrs_ave.append(np.mean(m_zcr))
    zcrs_std.append(np.std(m_zcr))
    m_rms = fRMS(fwav)
    rmss_min.append(np.min(m_rms))
    rmss_max.append(np.max(m_rms))
    rmss_ave.append(np.mean(m_rms))
    rmss_std.append(np.std(m_rms))

fig = plt.figure()
ax1 = fig.add_subplot(211)

ax1.bar(file,zcrs_max,0.2,label='zcr_max')
x=np.arange(4)+0.2  # 并列柱状图的关键，代表最小值在x轴位置
ax1.bar(x,zcrs_min,0.2,label='zcr_min')
x += 0.2            # 并列柱状图的关键，代表平均值在x轴位置
ax1.bar(x,zcrs_ave,0.2,label='zcr_ave')
x += 0.2            # 并列柱状图的关键，代表标准差在x轴位置
ax1.bar(x,zcrs_std,0.2,label='zcr_std')
ax1.set_ylabel("zcr") # 设置y轴代表内容
ax1.legend(loc="upper left")
#
ax1 = fig.add_subplot(212)
ax1.bar(file,rmss_max,0.2,label='rms_max')
x=np.arange(4)+0.2  # 并列柱状图的关键，代表最小值在x轴位置
ax1.bar(x,rmss_min,0.2,label='rms_min')
x += 0.2            # 并列柱状图的关键，代表平均值在x轴位置
ax1.bar(x,rmss_ave,0.2,label='rms_ave')
x += 0.2            # 并列柱状图的关键，代表标准差在x轴位置
ax1.bar(x,rmss_std,0.2,label='rms_std')
ax1.set_ylabel("rms") # 设置y轴代表内容
ax1.legend(loc="upper left")

plt.show()
