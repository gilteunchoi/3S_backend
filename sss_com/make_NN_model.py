import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Embedding, LSTM, Flatten
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.utils import plot_model
from tensorflow.keras.datasets import imdb
from tensorflow.keras.utils import plot_model, to_categorical

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

df1 = pd.read_excel('sss_com/first.xls', header=None)
df2 = pd.read_excel('sss_com/second.xls', header=None)
df3 = pd.read_excel('sss_com/third.xls', header=None)
df4 = pd.read_excel('sss_com/fourth.xls', header=None)

# bssid 추출
blist1 = []
blist2 = []
blist3 = []
blist4 = []

# rssid 추출
rlist1 = []
rlist2 = []
rlist3 = []
rlist4 = []

dataLength = int(len(df1)/2)  # 와이파이 측정 횟수 여기서는 100

for i in range(dataLength):
    for j in range(10):
        blist1.append(df1[j][2*i])
        blist2.append(df2[j][2*i])
        blist3.append(df3[j][2*i])
        blist4.append(df4[j][2*i])
        rlist1.append(df1[j][2*i+1])
        rlist2.append(df2[j][2*i+1])
        rlist3.append(df3[j][2*i+1])
        rlist4.append(df4[j][2*i+1])

print(blist1)
tempblist = blist1 + blist2 + blist3 + blist4  # 모든 bssid 리스트(중복O)
temprlist = rlist1 + rlist2 + rlist3 + rlist4  # 모든 bssid 리스트(중복O)
allbssidlist = []  # 모든 bssid 리스트(중복X)

temprlist = list(map(int, temprlist))
temprlist = list(map(abs, temprlist))

for v in tempblist:
    if v not in allbssidlist:
        allbssidlist.append(v)


with open('allbssidlist.txt', 'w') as f:
    f.write(json.dumps(allbssidlist))

lengthOfNodes = len(allbssidlist)  # 노드 갯수

# 전체 bssid 리스트 노드에 데이터 줄 세우기

tempnodelist = []  # 개별 데이터 리스트화

for i in range(len(tempblist)):
    for j in range(lengthOfNodes):
        # blist1 데이터가 전체 와이파이 노드중 어디에 매칭되냐 / j 는 노드의 인덱스
        if (tempblist[i] == allbssidlist[j]):
            tempnodelist.append(j)
            break
        if(j == lengthOfNodes-1):  # 새로운 데이터 올 때만 작동  / 매칭이 안된 것
            tempnodelist.append(-1)


finallist = []  # x train(can be xtest data too)

lengthOfAllWifiList = dataLength * 4  # 데이터 갯수 * 출구 개수(여기서는 4)

for i in range(lengthOfAllWifiList*10):  # 와이파이 데이터 개수 * 와이파이 10개
    if(i % 10 == 0):
        tempplist = [0 for j in range(lengthOfNodes)]   # 노드 갯수
    if(tempnodelist[i] != -1):
        # tempplist의 노드의 인덱스에만 그에 알맞는 rssi값 넣기
        tempplist[int(tempnodelist[i])] = temprlist[i]
    if((i+1) % 10 == 0):
        finallist.append(tempplist)

y1 = [0 for j in range(dataLength)]  # 1번출구
y2 = [1 for j in range(dataLength)]  # 2번출구
y3 = [2 for j in range(dataLength)]  # 3번출구
y4 = [3 for j in range(dataLength)]  # 4번출구

y = y1 + y2 + y3 + y4
y = list(map(int, y))

x_train = np.array(finallist)
y_train = np.array(y)

print(x_train[-1])
print(y_train)

y_train = to_categorical(y_train)  # 이게 중요
x_train = x_train.reshape(lengthOfAllWifiList, lengthOfNodes).astype(
    'float32')/100  # 284길이의 400개의 데이터를 0~1로 스케일 혹은 인코딩

model = Sequential([
    Dense(64, input_dim=lengthOfNodes, activation='relu'),
    Dense(32, activation='relu'),
    Dense(4, activation='softmax')
])

model.compile(loss='categorical_crossentropy',
              optimizer='adam', metrics=['accuracy'])

checkpoint_callback = ModelCheckpoint("best_model.h5", save_best_only=True, monitor="val_loss")

hist = model.fit(x_train, y_train, epochs=15, batch_size=32, 
                 validation_split=0.10, 
                 callbacks=[checkpoint_callback])