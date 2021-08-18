import pandas as pd
df1 = pd.read_excel('sss_com/first.xls',header=None)
df2 = pd.read_excel('sss_com/second.xls',header=None)
df3 = pd.read_excel('sss_com/third.xls',header=None)
df4 = pd.read_excel('sss_com/fourth.xls',header=None)

#bssid 추출
blist1=[]  
blist2=[]
blist3=[]
blist4=[]

#rssid 추출
rlist1=[]  
rlist2=[]
rlist3=[]
rlist4=[]

for i in range(100):
  for j in range(10):
    blist1.append(df1[j][2*i])
    blist2.append(df2[j][2*i])
    blist3.append(df3[j][2*i])
    blist4.append(df4[j][2*i])
    rlist1.append(df1[j][2*i+1])
    rlist2.append(df2[j][2*i+1])
    rlist3.append(df3[j][2*i+1])
    rlist4.append(df4[j][2*i+1])

tempblist = blist1 + blist2 + blist3 + blist4 #모든 bssid 리스트(중복O)
temprlist = rlist1 + rlist2 + rlist3 + rlist4 #모든 bssid 리스트(중복O)
allbssidlist=[]  #모든 bssid 리스트(중복X)
temprlist = list(map(int, temprlist))
temprlist = list(map(abs,temprlist))
minrssi = min(temprlist)

for i in range(len(temprlist)):   #스케일링
  if(temprlist[i] != 0):
    temprlist[i] = temprlist[i] - minrssi

for v in tempblist:
    if v not in allbssidlist:
        allbssidlist.append(v)

len(allbssidlist)  #노드 갯수

#노노노 listdf = pd.DataFrame([rlist1,blist1])

##### 전체 bssid 리스트 노드에 데이터 줄 세우기 

tempnodelist=[]
for i in range(len(tempblist)):
  for j in range(len(allbssidlist)):
    if (tempblist[i] == allbssidlist[j]):  #blist1 데이터가 전체 와이파이 노드중 어디에 매칭되냐 / j 는 노드의 인덱스
      tempnodelist.append(j)
      break
    if(j==len(allbssidlist)-1):         #새로운 데이터 올 때만 작동  / 매칭이 안된 것
      tempnodelist.append(-1)


finallist =  [] # x train(can be xtest data too) 


for i in range(4000):           #전체 데이터 길이
  if(i%10==0):
    tempplist = [0 for j in range(284)]   #284는 노드 갯수
  if(tempnodelist[i]!=-1):
    tempplist[int(tempnodelist[i])]=temprlist[i]  #tempplist의 노드의 인덱스에만 그에 알맞는 rssi값 넣기
  if((i+1)%10==0):
    finallist.append(tempplist)   

y1 = [0 for j in range(100)]  #1번출구
y2 = [1 for j in range(100)]  #1번출구
y3 = [2 for j in range(100)]  #1번출구
y4 = [3 for j in range(100)]  #1번출구

y = y1 + y2 + y3 + y4
y = list(map(int, y))

from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Embedding, LSTM, Flatten
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import plot_model
from tensorflow.keras.datasets import imdb
import matplotlib.pyplot as plt
import numpy as np
from tensorflow.keras.utils import plot_model, to_categorical

x_train = np.array(finallist)
y_train = np.array(y)

y_train = to_categorical(y_train)
x_train = x_train.reshape(400, 284).astype('float32') / 46.0

model = Sequential([
    Dense(64, input_dim=284, activation='relu'), 
    Dense(32, activation='relu'), 
    Dense(4, activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

checkpoint_callback = ModelCheckpoint("best_model.h5", 
                                      save_best_only=True, 
                                      monitor="val_loss")
